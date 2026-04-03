# https://github.com/Haoming02/sd-webui-forge-classic/tree/neo/extensions-builtin/sd_forge_spectrum
# https://github.com/wai55555/sd-webui-reforge-spectrum

import sys
import gradio as gr
from spectrum_core.forecaster import SpectrumSDXLCalibrated

from modules import scripts
from modules.infotext_utils import PasteField
from modules.ui_components import InputAccordion


class SpectrumScript(scripts.Script):
    def title(self):
        return "Calibrated Spectrum"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, *args, **kwargs):
        with InputAccordion(False, label=self.title()) as enable:
            with gr.Row():
                w = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.25,
                    step=0.05,
                    label="Prediction Weighting (w)",
                    info="higher = long-term trend ; lower = short-term changes",
                )
                m = gr.Slider(
                    minimum=1,
                    maximum=16,
                    value=6,
                    step=1,
                    label="Polynomial Degree (m)",
                    info="higher = complex & subtle patterns ; lower = stable & faster",
                )
            with gr.Row():
                lam = gr.Slider(
                    minimum=0.0,
                    maximum=2.0,
                    value=0.5,
                    step=0.05,
                    label="Regularization (lam)",
                    info="higher = reduce overfitting ; lower = fit more data",
                )
                window_size = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=2,
                    step=1,
                    label="Cache Window (window_size)",
                    info="higher = skip more steps ; lower = slower but more accurate",
                )
            flex_window = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.0,
                step=0.05,
                label="Window Growth (flex_window)",
                info="higher = more speed & less accurate ; lower = more consistent accuracy but less speed gain",
            )
            with gr.Row():
                warmup_steps = gr.Slider(
                    minimum=0,
                    maximum=20,
                    value=6,
                    step=1,
                    label="Warmup Steps",
                    info="Run the full model before caching starts",
                )
                stop_caching_step = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.9,
                    step=0.05,
                    label="Stop Caching Step",
                    info="Run the full model for the last few steps",
                )
            with gr.Row():
                enable_calibration = gr.Checkbox(
                    value=True,
                    label="Enable Calibration",
                )
                calibration_strength = gr.Slider(
                    minimum=0.0,
                    maximum=1.0,
                    value=0.5,
                    step=0.05,
                    label="Calibration Strength",
                    info="higher = more dark & thicker ; lower = more pale & thinner",
                )

        self.infotext_fields = [
            PasteField(enable, "spec_enable"),
            PasteField(w, "spec_w"),
            PasteField(m, "spec_m"),
            PasteField(lam, "spec_lam"),
            PasteField(window_size, "spec_window_size"),
            PasteField(flex_window, "spec_flex_window"),
            PasteField(warmup_steps, "spec_warmup_steps"),
            PasteField(stop_caching_step, "spec_stop_caching_step"),
            PasteField(enable_calibration, "spec_enable_calibration"),
            PasteField(calibration_strength, "spec_calibration_strength"),
        ]

        return [enable, w, m, lam, window_size, flex_window, warmup_steps, stop_caching_step, enable_calibration, calibration_strength]

    def process(self, p, enable: bool, *args):
        # ADetailer や Hires fix の二次パス等、本体以外の生成プロセスを検知
        # str(type(p)) による判定に加え、属性チェックを併用
        p_type_name = str(type(p))
        is_secondary = (
            getattr(p, "_in_adetailer", False) or 
            "Postprocessed" in p_type_name or 
            getattr(p, "is_hr_pass", False) # Hiresパスの明示的チェック
        )
        
        if is_secondary:
            self.remove_patch_force()
            return

        # 以前の状態を完全に破棄
        if hasattr(p, "_spectrum_state"):
            del p._spectrum_state
        p._spectrum_state = None
        
        if enable:
            # ログ出力を控えめにし、stdoutへの過剰な干渉を避ける
            # (reForge の時間計測が stdout の進捗バーをパースしている可能性があるため)
            sys.stdout.write("[Spectrum] Enabled for main sampling.\n")
            sys.stdout.flush()
        else:
            self.remove_patch_force()

    def process_before_every_sampling(self, p, enable: bool, *args, **kwargs):
        if not enable:
            return

        # 二次プロセスのガード (ADetailer 等)
        p_type_name = str(type(p))
        if getattr(p, "_in_adetailer", False) or "Postprocessed" in p_type_name:
            return

        unet = p.sd_model.forge_objects.unet
        unet = SpectrumSDXLCalibrated.patch(unet, p.steps, *args)
        p.sd_model.forge_objects.unet = unet

        p.extra_generation_params["spec_enable"] = True
        for k, v in zip([
        "spec_w", "spec_m", "spec_lam", "spec_window_size", "spec_flex_window",
        "spec_warmup_steps", "spec_stop_caching_step",
        "spec_enable_calibration", "spec_calibration_strength"], args):
            p.extra_generation_params[k] = v

    def remove_patch_force(self):
        import modules.shared as shared
        # shared.sd_model だけでなく、現在のアクティブなモデルからも取得を試みる
        unet = getattr(getattr(shared.sd_model, "forge_objects", None), "unet", None)
        if not unet:
            return
            
        # 完全にキーを削除してサンプラーを元の状態に戻す
        if "model_function_wrapper" in unet.model_options:
            wrap = unet.model_options["model_function_wrapper"]
            # 自分のラッパー、あるいは異常な None の場合に削除
            if wrap is None or (hasattr(wrap, "__name__") and wrap.__name__ == "spectrum_unet_wrapper"):
                del unet.model_options["model_function_wrapper"]
                print("[Spectrum] Extension DISABLED. UNet patch removed safely.")
        
        # Forgeの内部データ構造もクリア
        try:
            if hasattr(unet, "set_model_unet_function_wrapper"):
                # 内部辞書の書き換えを伴うため、Noneをセットせず直接辞書を触ったあとに状態のみリセット
                pass
        except Exception:
            pass

