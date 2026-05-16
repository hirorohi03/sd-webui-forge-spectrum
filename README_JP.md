# sd-webui-forge-spectrum (Calibrated Spectrum Adaptive Forecaster [LEGACY])

<div align="center">

### [🇺🇸 English](README.md) | [🇯🇵 日本語](README_JP.md) 

</div>

[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)の`SpectrumSDXLCalibrated`ノードをStable Diffusion WebUI Forge/reForgeの拡張機能として動作するよう移植したものです（A1111では動作しません）。

---

## ⚠️ 重要なお知らせ

オリジナルの[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)の[2026年5月3日の更新](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl/commit/b7ac6ca0b5d9333a6f19527f6b1b3dfa256cbadb)において、`SpectrumSDXLCalibrated`ノードが**レガシー／非準拠ノード**に設定されました。

[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)には二つのノードがあり、当拡張機能は `SpectrumSDXLCalibrated` を移植したものです。

- `SpectrumSDXLC`
    - [公式のforecasterコード](https://github.com/hanjq17/Spectrum/blob/main/src/utils/basis_utils.py)の忠実な実装
    - こちらの移植版は[sd-forge-spectrum-faithful](https://github.com/hirorohi03/sd-forge-spectrum-faithful)で公開済み
- `SpectrumSDXLCalibrated` （レガシー／非準拠ノード）
    - 「キャリブレーション」などの[論文](https://arxiv.org/abs/2603.01623)に忠実ではない原則に反した機能を実装
    - 当拡張機能はこちらを移植したもの

以下は、2026年5月3日に更新された[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)のREADMEから抜粋して翻訳したものです。

> **レガシー／非準拠ノード：**`SpectrumSDXLCalibrated`ノードは、現在**レガシー**と見なされています。
> 
> *リピーターの方への説明：* このノードの以前のバージョンは、当初公式のforecaster実装を見つけることができなかったため、実質的にゼロから「バイブコーディング」されたものでした。その結果、「キャリブレーション」のような、興味深いものの論文に忠実ではない、いくらか原則に反する追加が行われてしまいました。この問題は、[公式のforecasterコード](https://github.com/hanjq17/Spectrum/blob/main/src/utils/basis_utils.py)を`SpectrumSDXL`ノードに移植することで解決されました。より安定的で原則に基づいた結果を得るため、この正確な実装へ移行してください。

`SpectrumSDXLCalibrated`ノードの移植版である当拡張機能も、**レガシー／非準拠**な拡張機能とします。

機能と性能は特に変更ありませんが、UIに **[LEGACY]** という表示が追加されます。**レガシー／非準拠**な拡張機能であることをご認識のうえでご利用ください。

### 🆕 New!
`SpectrumSDXL`**ノードをForge/reForgeの拡張機能として移植したものを[sd-forge-spectrum-faithful](https://github.com/hirorohi03/sd-forge-spectrum-faithful)にて公開しました。よろしければ使ってみてください。**

---

## 🚀 概要

Spectrum機能と、[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)が独自に実装しているCalibration機能を利用し、画質劣化と画像変化を最小に抑えながら画像生成の生成時間を削減できます。

SDXL (Forge, reForge, Forge Neo)、およびAnima (Forge Neo) を利用した画像生成で動作することを確認しています。

技術の詳細については[ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl)や[Spectrumのプロジェクトページ](https://hanjq17.github.io/Spectrum/)などを参照してください。

Forge/reForgeへの移植にあたっては以下の拡張機能の実装を参考にしました。
- [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)のSpectrum Integrated
- [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum)

## 📖 更新履歴

### 2026/5/16

- 他のSpectrum拡張機能と同時にインストールしてもエラーが発生しないようにしました（同時に有効にして生成した場合の動作は保証しません）。
    - [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum)
    - [sd-forge-spectrum-faithful](https://github.com/hirorohi03/sd-forge-spectrum-faithful)
- UIでの機能名を`Calibrated Spectrum [LEGACY]`から`Calibrated Spectrum Adaptive Forecaster [LEGACY]`に変更しました。

### 2026/5/14

- UIでの機能とCalibration設定の名称に[LEGACY]を追加しました。
    - 処理内容に変更はありません。
- [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo) Spectrum Integratedのエラー処理をマージしました。
    - [Commits cd837f4 on May 14, 2026](https://github.com/Haoming02/sd-webui-forge-classic/commit/cd837f4fedf302bb160d23fe82bd15e457b1e6b9)
    - Forge Neoの`Settings`の`Ignore Negative Prompt During Later Steps`または`Skip Negative Prompt During Later Steps`と併用した場合のエラー処理。

## 📊 性能比較
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

- いずれも少し異なる画像が生成されます。
- Calibration Strengthを高くするとアーティファクトを生成することが他より多いかもしれません。

## 📦 インストール方法
1. WebUIの**Extensions**タブを開きます。
2. **Install from URL**を選択します。
3. https://github.com/hirorohi03/sd-webui-forge-spectrum.git を入力し、**Install**をクリックします。
4. **Installed**を選択します。
5. **Apply and quit**をクリックします。
6. WebUIを再起動します。

## 🖼️ 使用方法
txt2imgまたはimg2imgのCalibrated Spectrumタブのチェックボックスをチェックし、パラメータを設定して生成してください。

## 🛠️ パラメータ設定と推奨値

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

[Anima Turbo LoRA](https://civitai.com/models/2560840/)や[DMD2 LoRA](https://civitai.com/models/2466415/)などのステップ数削減LoRAと併用する場合はWarmup Stepsを1～2に減らしてください。

## ⚠️ 既知の制約

- この拡張機能は以下のSpectrum機能と競合せずインストールできますが、同時に有効にして生成した場合の動作は保証しません。
    - [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo)のSpectrum Integrated
    - [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum)
    - [sd-forge-spectrum-faithful](https://github.com/hirorohi03/sd-forge-spectrum-faithful)
- Forge Neoの`Settings`の`Ignore Negative Prompt During Later Steps`または`Skip Negative Prompt During Later Steps`と併用した場合にエラーが発生する可能性があります。

## 📜 クレジットと参考文献
*   **論文**: [Adaptive Spectral Feature Forecasting for Diffusion Sampling Acceleration](https://arxiv.org/abs/2603.01623)
*   **プロジェクトページ**: [https://hanjq17.github.io/Spectrum/](https://hanjq17.github.io/Spectrum/)
*   **公式リポジトリ**: [hanjq17/Spectrum](https://github.com/hanjq17/Spectrum)
*   **ComfyUI 実装**: [ComfyUI Spectrum SDXL Node](https://github.com/ruwwww/ComfyUI-Spectrum-sdxl) by [A. Izzuddin Al Faruq](https://github.com/ruwwww/)
*   **移植コードの参考**: [sd-webui-reforge-spectrum](https://github.com/wai55555/sd-webui-reforge-spectrum) by [wai55555](https://github.com/wai55555)
*   **移植コードの参考**: [Forge Neo](https://github.com/Haoming02/sd-webui-forge-classic/tree/neo) Spectrum Integrated by [Haoming](https://github.com/Haoming02)

## ⚖️ ライセンス
本プロジェクトは **MIT License** の下で公開されています。
