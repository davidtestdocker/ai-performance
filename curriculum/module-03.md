# 模組 03：GPU 架構與 C++／CUDA 微基準

[路線](ROADMAP.md)｜目標：理解 GPU 計算與資料移動的代價，能用 C++/CUDA 程式驗證假設。

[觀念講義](CONCEPTS.md)第 03 節｜[作品成果](OUTCOMES.md)

## 學習大綱

GPU 執行階層與記憶體 → C++ 正確性基準 → CUDA kernel → 分段計時與有效頻寬 → profiler 指標 → 調整與複測。

## 先理解

SM、warp、block、global/shared memory、coalescing、H2D/D2H、PCIe、算術強度與有效頻寬；區分理論峰值、實測有效頻寬、kernel 時間和應用端到端時間。[CUDA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)

## 實作順序

1. 寫 CPU 參考版和 CUDA 版的向量／stencil 工作，對多種輸入大小驗證數值誤差與邊界條件。
2. 分別量測 H2D、kernel、D2H、端到端時間；計算實際讀寫 bytes 與有效頻寬。
3. 比較至少兩種資料布局或 block size，先預測哪個瓶頸會變化，再跑受控 A/B。
4. 使用 Nsight Compute 可取得的 kernel 指標檢驗推測；若受權限或硬體限制，保留 CUDA event、正確性與限制說明。[Nsight Compute](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html)
5. 把本模組的資料移動模型用於模組 04–06 的訓練 trace 判讀。

## 做完留下的成果

CPU/GPU 答案相符；有分段時間、有效頻寬曲線、至少一輪假設與複測；能解釋最快 kernel 為何未必帶來最快端到端訓練。單卡結果不得寫成多 GPU 通訊結果。
