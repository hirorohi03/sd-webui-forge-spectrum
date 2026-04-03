# sd-webui-forge-spectrum (Calibrated Spectrum)

[日本語版はこちら (README_JP.md)](README_JP.md)

This is a port of the [ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl) designed to run as an extension for Stable Diffusion WebUI Forge/reForge (it does not work on A1111). <BR>
I have confirmed that it works for image generation using SDXL on Forge, reForge, and Forge Neo (I believe it also works for image generation using Anima and similar tools on Forge Neo).

By utilizing the Spectrum feature and the Calibration feature uniquely implemented by the ComfyUI Spectrum SDXL Node, you can reduce image generation time while minimizing image degradation and visual changes. <BR>
For technical details, please refer to the [ComfyUI Spectrum SDXL Node GitHub](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl) or the [Spectrum project page](https://hanjq17.github.io/Spectrum/).

When porting to Forge/reForge, I referred to the implementation of the following extensions:
- [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo) Spectrum Integrated
- [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum)

## 🖼 Performance comparison
**SDXL Calibrated Comparisons (30-step Euler)**
| Normal | Spectrum | Calibrated (strength 0.5) | Calibrated (strength 0.8) |
| :----: | :------: | :----------------------: | :----------------------: |
| ![Normal1](/images/1_nocache.png) | ![Spectrum1](/images/1_spectrum.png) | ![Calibrated0.5_1](/images/1_calibrated05.png) | ![Calibrated0.8_1](/images/1_calibrated08.png) |
| **3.14 s** | **2.00 s** | **2.01 s** | **1.98 s** |
| ![Normal2](/images/2_nocache.png) | ![Spectrum2](/images/2_spectrum.png) | ![Calibrated0.5_2](/images/2_calibrated05.png) | ![Calibrated0.8_2](/images/2_calibrated08.png) |
| **3.19 s** | **1.90 s** | **1.86 s** | **1.88 s** |

## 📦 Installation
1. Open the **Extensions** tab in your WebUI.
2. Select **Install from URL**.
3. Enter https://github.com/hirorohi03/sd-webui-forge-spectrum.git and click **Install**.
4. Select **Installed**.
5. Click **Apply and quit**.
6. Restart your WebUI.

## How to Use
Check the checkbox in the “Calibrated Spectrum” tab of txt2img or img2img, set the parameters, and generate the image.

## 🛠 Parameter Settings and Recommended Values

| Parameter | Range | Default | Description |
| :--- | :--- | :--- | :--- |
| **Prediction Weighting<BR>`w`** | 0.0 - 1.0 | **0.25** | Prediction weight<BR>High: Smoothing, Low (0.4–0.5): Maintains sharpness |
| **Polynomial Degree<BR>`m`** | 1 - 8 | **6** | Coefficients of Chebyshev polynomial basis functions<BR>High: Complex & delicate, Low (3): Fast & stable |
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
