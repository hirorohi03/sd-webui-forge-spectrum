# https://github.com/ruwwww/comfyui-spectrum-sdxl

import math
import torch

# ====================== Spectrum with Residual Calibration ======================
class CalibratedFastChebyshevForecaster:
    def __init__(self, m: int, lam: float, steps: int):
        self.M = m
        self.K = max(m + 2, 8)
        self.lam = lam
        self.H_buf = []
        self.T_buf = []
        self.shape = None
        self.dtype = None
        self.t_max = float(steps)
        self.residual = None
        self.last_raw_guess = None

    def _taus(self, t: float) -> float:
        return (t / self.t_max) * 2.0 - 1.0

    def _build_design(self, taus: torch.Tensor) -> torch.Tensor:
        taus = taus.reshape(-1, 1)
        T = [torch.ones((taus.shape[0], 1), device=taus.device, dtype=torch.float32)]
        if self.M > 0:
            T.append(taus)
            for _ in range(2, self.M + 1):
                T.append(2 * taus * T[-1] - T[-2])
        return torch.cat(T[: self.M + 1], dim=1)

    def update(self, cnt: int, h: torch.Tensor):
        if self.shape and h.shape != self.shape:
            self.reset_buffers()

        self.shape = h.shape
        self.dtype = h.dtype

        self.H_buf.append(h.detach().view(-1))
        self.T_buf.append(self._taus(cnt))
        if len(self.H_buf) > self.K:
            self.H_buf.pop(0)
            self.T_buf.pop(0)

    def predict(self, cnt: int, w: float, enable_calibration: bool = False, calibration_strength: float = 0.5, use_calibration: bool | None = None) -> torch.Tensor:
        if use_calibration is not None:
            enable_calibration = use_calibration

        device = self.H_buf[-1].device

        H = torch.stack(self.H_buf, dim=0).to(torch.float32)
        T = torch.tensor(self.T_buf, dtype=torch.float32, device=device)

        P = self.M + 1
        X = self._build_design(T)
        lamI = self.lam * torch.eye(P, device=device)
        XtX = X.T @ X + lamI

        try:
            L = torch.linalg.cholesky(XtX)
        except RuntimeError:
            jitter = 1e-6 * XtX.diag().mean()
            L = torch.linalg.cholesky(XtX + jitter * torch.eye(P, device=device))

        XtH = X.T @ H
        coef = torch.cholesky_solve(XtH, L)

        tau_star = torch.tensor([self._taus(cnt)], device=device)
        pred_cheb = (self._build_design(tau_star) @ coef).squeeze(0)

        h_i = self.H_buf[-1]
        h_taylor = h_i + (h_i - self.H_buf[-2]) if len(self.H_buf) >= 2 else h_i

        # EXACT Official Logic: Always blend using `w`, even if history is incomplete.
        # No dynamic degree clamping, no value clamping.
        raw_guess = (1 - w) * h_taylor + w * pred_cheb
            
        self.last_raw_guess = raw_guess.detach().clone()

        if enable_calibration and self.residual is not None:
            effective_residual = self.residual.to(device=device, dtype=torch.float32) * calibration_strength
            final_pred = raw_guess + effective_residual
        else:
            final_pred = raw_guess

        return final_pred.to(self.dtype).view(self.shape)

    def reset_buffers(self):
        self.H_buf.clear()
        self.T_buf.clear()
        self.shape = None
        self.dtype = None
        self.residual = None
        self.last_raw_guess = None


class SpectrumSDXLCalibrated:

    @staticmethod
    def patch(model, steps: int, w: float, m: int, lam: float, window_size: int, flex_window: float, warmup_steps: int, stop_caching_step: float, enable_calibration, calibration_strength: float):
        state = getattr(model, 'spectrum_state', {})
        model.spectrum_state = state

        state = {
            "forecasters": None,
            "cnt": 0,
            "num_cached": [0],
            "curr_ws": float(window_size),
            "last_t": -1,
            "total_runs": 0,
        }

        # Remove any lingering hooks from previously bypassed models to clear global memory leaks
        diffusion_model = model.model.diffusion_model
        if hasattr(diffusion_model, "_sp_hooks"):
            for h in diffusion_model._sp_hooks: h.remove()
            diffusion_model._sp_hooks = []
        if hasattr(diffusion_model, "spectrum_hook_handles"):
            for h in diffusion_model.spectrum_hook_handles: h.remove()
            diffusion_model.spectrum_hook_handles = []

        forecast_stream = torch.cuda.Stream() if torch.cuda.is_available() else None

        def _batch_index_tensor(mask: torch.Tensor) -> torch.Tensor:
            return mask.nonzero(as_tuple=False).flatten()

        def _slice_if_batch(value, index_tensor, batch_size):
            if isinstance(value, torch.Tensor) and value.dim() > 0 and value.shape[0] == batch_size:
                return value[index_tensor.to(value.device)]
            return value

        def spectrum_unet_wrapper(model_function, kwargs):
            x, timestep, c = kwargs["input"], kwargs["timestep"], kwargs["c"]
            batch_size = x.shape[0]
            if isinstance(timestep, torch.Tensor):
                t_scalar = timestep.flatten()[0].item()
            else:
                t_scalar = float(timestep)

            if t_scalar > state["last_t"]:
                state["forecasters"] = None
                state["cnt"] = 0
                state["num_cached"] = [0] * batch_size
                state["curr_ws"] = float(window_size)
                state["total_runs"] += 1

            state["last_t"] = t_scalar

            if state["forecasters"] is None:
                state["forecasters"] = [CalibratedFastChebyshevForecaster(m=m, lam=lam, steps=steps) for _ in range(batch_size)]

            if len(state["num_cached"]) != batch_size:
                state["num_cached"] = [0] * batch_size

            do_actual = torch.ones(batch_size, dtype=torch.bool, device=x.device)
            for i in range(batch_size):
                is_micro_final = False
                auto_stop = int(steps * stop_caching_step)
                if state["cnt"] >= auto_stop:
                    is_micro_final = True

                if state["cnt"] >= warmup_steps and not is_micro_final:
                    do_actual[i] = (state["num_cached"][i] + 1) % max(1, math.floor(state["curr_ws"])) == 0

            real_mask = do_actual
            forecast_mask = ~do_actual

            out = torch.empty_like(x)

            # ====================== REAL STEP: Run full diffusion_model → capture RAW 4D tensor (post final_layer/unpatchify) ======================
            if real_mask.any():
                real_indices = _batch_index_tensor(real_mask)
                x_real = x[real_mask]
                timestep_real = _slice_if_batch(timestep, real_indices, batch_size)
                c_real = {k: _slice_if_batch(v, real_indices, batch_size) for k, v in c.items()}

                out_real = model_function(x_real, timestep_real, **c_real)
                out[real_mask] = out_real

                real_indices_list = real_indices.tolist()
                for j, idx in enumerate(real_indices_list):
                    forecaster = state["forecasters"][idx]
                    if enable_calibration and forecaster.last_raw_guess is not None:
                        forecaster.residual = out_real[j].detach().view(-1).to(torch.float32) - forecaster.last_raw_guess
                    forecaster.update(state["cnt"], out_real[j])
                    state["num_cached"][idx] = 0

            # ====================== SKIP STEP: Forecast RAW tensor ======================
            if forecast_mask.any():
                forecast_indices = _batch_index_tensor(forecast_mask).tolist()
                out_forecast = torch.empty((len(forecast_indices), *x.shape[1:]), device=x.device, dtype=x.dtype)

                if forecast_stream:
                    with torch.cuda.stream(forecast_stream):
                        for j, idx in enumerate(forecast_indices):
                            out_forecast[j] = state["forecasters"][idx].predict(state["cnt"], w, enable_calibration=enable_calibration, calibration_strength=calibration_strength)
                        out[forecast_mask] = out_forecast
                        for idx in forecast_indices:
                            state["num_cached"][idx] += 1
                    torch.cuda.current_stream().wait_stream(forecast_stream)
                else:
                    for j, idx in enumerate(forecast_indices):
                        out_forecast[j] = state["forecasters"][idx].predict(state["cnt"], w, enable_calibration=enable_calibration, calibration_strength=calibration_strength)
                    out[forecast_mask] = out_forecast
                    for idx in forecast_indices:
                        state["num_cached"][idx] += 1

            if state["cnt"] >= warmup_steps:
                state["curr_ws"] += flex_window

            state["cnt"] += 1
            return out

        new_model = model.clone()

        # SAFEGUARD: Deepcopy model_options to prevent the wrapper from permanently
        # mutating the globally cached CheckpointLoader model in memory.
        import copy
        if hasattr(model, 'model_options'):
            new_model.model_options = copy.deepcopy(model.model_options)

        new_model.set_model_unet_function_wrapper(spectrum_unet_wrapper)
        return new_model
