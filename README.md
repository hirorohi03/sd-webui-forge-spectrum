# sd-webui-forge-spectrum (Calibrated Spectrum)

<div align="center">

### [🇺🇸 English](README.md) | [🇯🇵 日本語](README_JP.md) 

</div>

This is a port of the `SpectrumSDXLCalibrated` node from [ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl) to run as an extension for Stable Diffusion WebUI Forge/reForge (it does not work on A1111). 

---

## ⚠️ Important Information

In the [May 3, 2026 update](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl/commit/b7ac6ca0b5d9333a6f19527f6b1b3dfa256cbadb) to the original [ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl), It has been announced that `SpectrumSDXLCalibrated` node has been set to **Legacy / Non-Faithful Node**.

There are two nodes in [ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl), and this extension is a port of `SpectrumSDXLC`.

- `SpectrumSDXLC`
    - Porting of the [official forecaster code](https://github.com/hanjq17/Spectrum/blob/main/src/utils/basis_utils.py)
    - This port has already been released as [sd-forge-spectrum-faithful](https://github.com/hirorohi03/sd-forge-spectrum-faithful)
- `SpectrumSDXLCalibrated` （レガシー／非準拠ノード）
    - There are some non-principled additions like "calibration" which are not faithful to the [paper](https://arxiv.org/abs/2603.01623)
    - This extension is a port of this one

The following is an excerpt from the README for [ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl), updated on May 3, 2026.

> **Legacy / Non-Faithful Node:** The `SpectrumSDXLCalibrated` node is now considered **legacy**. 
> 
> *Clarification for returning users:* The previous version of this node was essentially "vibe-coded" from scratch because I couldn't initially find the official forecaster implementation. This led to some non-principled additions like "calibration" which, while interesting, are not faithful to the paper. This has now been solved by porting the [official forecaster code](https://github.com/hanjq17/Spectrum/blob/main/src/utils/basis_utils.py) into the `SpectrumSDXL` node. Please migrate to the faithful implementation for more stable and principled results.

This extension, which is a port of`SpectrumSDXLCalibrated` node, has been also set to **Legacy / Non-Faithful** extension.

There are no specific changes to functionality or performance, but the label **[LEGACY]** will be added to the UI. Please use this extension with the understanding that it is a **Legacy / Non-Faithful** extension.

### 🆕 New
**I have released a port of the** `SpectrumSDXL` **node as a Forge/reForge extension at [sd-forge-spectrum-faithful](https://github.com/hirorohi03/sd-forge-spectrum-faithful). Please give it a try.**

---

I have confirmed that it works for image generation using SDXL (Forge, reForge, Forge Neo) and Anima (Forge Neo). I think this extension will work with other image generation models as well.

By utilizing the Spectrum feature and the Calibration feature uniquely implemented by the ComfyUI Spectrum SDXL Node, you can reduce image generation time while minimizing image degradation and visual changes. <BR>
For technical details, please refer to the [ComfyUI Spectrum SDXL Node GitHub](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl) or the [Spectrum project page](https://hanjq17.github.io/Spectrum/).

When porting to Forge/reForge, I referred to the implementation of the following extensions:
- [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo) Spectrum Integrated
- [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum)

## 📊 Performance comparison
- Stable Diffusion WebUI Forge - Neo v2.17
- Python 3.13.12
- PyTorch 2.10.0+cu130
- SageAttention 2
- RTX 5090 

**waiIllustriousSDXL_v160 (30-step Euler)**
| Normal |  Spectrum | Calibrated (strength 0.5) | Calibrated (strength 0.8) |
| :---: | :---: | :---: | :---: |
| ![Normal1](/images/sdxl1_normal.png) | ![Spectrum1](/images/sdxl1_spec.png) | ![Calibrated0.5_1](/images/sdxl1_cal05.png) | ![Calibrated0.8_1](/images/sdxl1_cal08.png) |
| **3.30 s** | **1.99 s** | **2.03 s** | **1.98 s** |
| ![Normal2](/images/sdxl2_normal.png) | ![Spectrum2](/images/sdxl2_spec.png) | ![Calibrated0.5_2](/images/sdxl2_cal05.png) | ![Calibrated0.8_2](/images/sdxl2_cal08.png) |
| **3.28 s** | **1.91 s** | **1.81 s** | **1.92 s** |

**anima-preview (30-step er-sde)**
| Normal  | Spectrum | Calibrated (strength 0.5) |
| :---: | :---: | :---: |
| ![Anima_Normal](/images/anima_normal.png) | ![Anima_Spec](/images/anima_spec.png) | ![Anima_Cal0.5](/images/anima_cal05.png) |
| **6.56 s** | **3.47 s** | **3.49 s** |

- Each one generates slightly different images.
- Setting the Calibration Strength to a high value may generate more artifacts than others.

## 📦 Installation
1. Open the **Extensions** tab in your WebUI.
2. Select **Install from URL**.
3. Enter https://github.com/hirorohi03/sd-webui-forge-spectrum.git and click **Install**.
4. Select **Installed**.
5. Click **Apply and quit**.
6. Restart your WebUI.

## 🖼️ How to Use
Check the checkbox in the “Calibrated Spectrum” tab of txt2img or img2img, set the parameters, and generate the image.

## 🛠️ Parameter Settings and Recommended Values
| Parameter | Range | Default | Description |
| :--- | :--- | :--- | :--- |
| **Prediction Weighting<BR>`w`** | 0.0 - 1.0 | **0.25** | Prediction weight<BR>High: Smoothing, Low (0.4–0.5): Maintains sharpness |
| **Polynomial Degree<BR>`m`** | 1 - 16 | **6** | Coefficients of Chebyshev polynomial basis functions<BR>High: Complex & delicate, Low (3): Fast & stable |
| **Regularization<BR>`lam`** | 0 - 2 | **0.5** | Ridge regularization strength (λ)<BR>High (1): Prevents latent explosion, rainbow artifacts, and black output in low-precision mode |
| **Cache Window<BR>`window_size`** | 1 - 10 | **2** | Initial prediction window size (number of steps to skip)<BR>High: Fast & low accuracy, Low: Slow & high accuracy |
| **Window Growth<BR>`flex_window`** | 0.0 - 2.0 | **0.00** | Incremental value added to the window after each UNet path execution<BR>High: Fast & low accuracy, Low: Slow & high accuracy |
| **Warmup Steps<BR>`warmup_steps`** | 0 - 20 | **6** | Number of initial full model execution steps before starting prediction<BR>High: Stable, Low: Fast |
| **Stop Caching Step<BR>`stop_caching_step`** | 0.0 - 1.0 | **0.90** | Number of steps at which prediction stops and returns to full model execution<BR>Specified as a percentage of the total number of steps |
| **Enable Calibration<BR>`enable_calibration`** | True / False | **True** | Enable/Disable calibration |
| **Calibration Strength<BR>`calibration_strength`** | 0.0 - 1.0 | **0.5** | Calibration strength<BR>High: Thick & Bold, Low: Thin & Light |

## 📜 Credits & References
*   **Paper**: [Adaptive Spectral Feature Forecasting for Diffusion Sampling Acceleration](https://arxiv.org/abs/2603.01623)
*   **Project Page**: [https://hanjq17.github.io/Spectrum/](https://hanjq17.github.io/Spectrum/)
*   **Official Implementation**: [hanjq17/Spectrum](https://github.com/hanjq17/Spectrum)
*   **ComfyUI Implementation**: [ruwwww/ComfyUI-Spectrum-sdxl](https://github.com/ruwwww/comfyui-spectrum-sdxl)

## ⚖️ License
This project is licensed under the **MIT License**.
