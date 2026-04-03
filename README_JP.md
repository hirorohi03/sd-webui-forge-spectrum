# sd-webui-forge-spectrum (Calibrated Spectrum)

[English README is here](README.md)

[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)をStable Diffusion WebUI Forge/reForgeの拡張機能として動作するよう移植したものです（A1111では動作しません）。<BR>
SDXL (Forge, reForge, Forge Neo)、およびAnima (Forge Neo) を利用した画像生成で動作することを確認しています。他の画像生成モデルでも動作するものがあると思います。

Spectrum機能と、ComfyUI Spectrum SDXL Nodeが独自に実装しているCalibration機能を利用し、画質劣化と画像変化を最小に抑えながら画像生成の生成時間を削減できます。<BR>
技術の詳細については[ComfyUI Spectrum SDXL NodeのGIthub](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)や[Spectrumのプロジェクトページ](https://hanjq17.github.io/Spectrum/)などを参照してください。

Forge/reForgeへの移植にあたっては以下の拡張機能の実装を参考にしました。
- [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)のSpectrum Integrated
- [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum)

## 🖼 性能比較
- Stable Diffusion WebUI Forge - Neo v2.17
- Python 3.13.12
- PyTorch 2.10.0+cu130
- SageAttention 2
- RTX 5090 

**SDXL (30-step Euler)**
| Normal |  Spectrum | Calibrated (strength 0.5) | Calibrated (strength 0.8) |
| :---: | :---: | :---: | :---: |
| ![Normal1](/images/sdxl1_normal.png) | ![Spectrum1](/images/sdxl1_spec.png) | ![Calibrated0.5_1](/images/sdxl1_cal05.png) | ![Calibrated0.8_1](/images/sdxl1_cal08.png) |
| **3.30 s** | **1.99 s** | **2.03 s** | **1.98 s** |
| ![Normal2](/images/sdxl2_normal.png) | ![Spectrum2](/images/sdxl2_spec.png) | ![Calibrated0.5_2](/images/sdxl2_cal05.png) | ![Calibrated0.8_2](/images/sdxl2_cal08.png) |
| **3.28 s** | **1.91 s** | **1.81 s** | **1.92 s** |

**Anima (30-step er-sde)**
| Normal  | Spectrum | Calibrated (strength 0.5) |
| :---: | :---: | :---: |
| ![Anima_Normal](/images/anima_normal.png) | ![Anima_Spec](/images/anima_spec.png) | ![Anima_Cal0.5](/images/anima_cal05.png) |
| **6.56 s** | **3.47 s** | **3.49 s** |

## 📦 インストール方法
1. WebUIの**Extensions**タブを開きます。
2. **Install from URL**を選択します。
3. https://github.com/hirorohi03/sd-webui-forge-spectrum.git を入力し、**Install**をクリックします。
4. **Installed**を選択します。
5. **Apply and quit**をクリックします。
6. WebUIを再起動します。

## 使用方法
txt2imgまたはimg2imgのCalibrated Spectrumタブのチェックボックスをチェックし、パラメータを設定して生成してください。

## 🛠 パラメータ設定と推奨値

| パラメータ | 範囲 | 初期値 | 説明 |
| :--- | :--- | :--- | :--- |
| **Prediction Weighting<BR>`w`** | 0.0 - 1.0 | **0.25** | 予測の重み<BR>高：平滑化、低 (0.4～0.5)：シャープネス維持 |
| **Polynomial Degree<BR>`m`** | 1 - 16 | **6** | チェビシェフ多項式の基底関数の係数<BR>高：複雑＆繊細、低 (3)：高速＆安定 |
| **Regularization<BR>`lam`** | 0 - 2 | **0.5** | リッジ正則化強度 (λ)<BR>高 (1)：低精度モードでのlatent爆発、レインボーアーティファクト、黒出力を防止 |
| **Cache Window<BR>`window_size`**| 1 - 10 | **2** | 初期予測ウィンドウサイズ（スキップするステップ数）<BR>高：高速＆低精度、低：低速＆高精度 |
| **Window Growth<BR>`flex_window`** | 0.0 - 2.0 | **0.00** | 各UNetパス実行後にウィンドウに加算する増分値<BR>高：高速＆低精度、低：低速＆高精度 |
| **Warmup Steps<BR>`warmup_steps`** | 0 - 20 | **6** | 予測開始前の初期フルモデル実行ステップ数<BR>高：安定、低：高速 |
| **Stop Caching Step<BR>`stop_caching_step`** | 0.0 - 1.0 | **0.90** | 予測を停止しフルモデル実行に戻すステップ数<BR>全ステップ数に対する割合で指定 |
| **Enable Calibration<BR>`enable_calibration`** | True / False | **True** | Calibrationの有効／無効 |
|  **Calibration Strength<BR>`calibration_strength`** | 0.0 - 1.0 | **0.5** | Calibrationの強さ<BR>高：濃く＆太く、低：薄く＆細く |

## 📜 クレジットと参考文献
*   **論文**: [Adaptive Spectral Feature Forecasting for Diffusion Sampling Acceleration](https://arxiv.org/abs/2603.01623)
*   **プロジェクトページ**: [https://hanjq17.github.io/Spectrum/](https://hanjq17.github.io/Spectrum/)
*   **公式リポジトリ**: [hanjq17/Spectrum](https://github.com/hanjq17/Spectrum)
*   **ComfyUI 実装**: [ruwwww/ComfyUI-Spectrum-sdxl](https://github.com/ruwwww/comfyui-spectrum-sdxl)

## ⚖️ ライセンス
本プロジェクトは **MIT License** の下で公開されています。
