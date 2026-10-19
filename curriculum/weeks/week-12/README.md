# 第 12 週：ML 訓練效能 Profiling

[固定課綱](../../ROADMAP.md)｜[進度](../../../PROGRESS.md)｜[帶練規則](../../TEACHING.md)

**固定目標：** 拆解資料、搬移、forward/backward 與 optimizer 的成本。

**職缺對應：** B ML 效能分析；A 可信量測

**設備：** 一張 NVIDIA GPU

**先備：** 前 11 週必要驗收通過；新工具仍從最小例子開始。

| 日 | 主題 | 可觀察驗收 |
|---|---|---|
| [D01](day-01/README.md) | 訓練指標與基線 | 至少五次獨立短跑，計時外處理啟動，保存 loss 與正確性訊號。 |
| [D02](day-02/README.md) | PyTorch Profiler | 能讀出主要 operators 與 GPU 空檔，profiler run 不與正式速度混用。 |
| [D03](day-03/README.md) | DataLoader 瓶頸 | 兩路徑模型與樣本 shape 一致，假資料只用於診斷、不冒充真實吞吐。 |
| [D04](day-04/README.md) | Pinned memory 與傳輸 | 同資料與 batch，比對 end-to-end；無改善也保留，不只報 memcpy 時間。 |
| [D05](day-05/README.md) | ML 診斷驗收 | 能用 trace 支持瓶頸，loss/validation 無未解釋退化，現場改 batch 後能重新判讀。 |

## 本週成果與通關

必交：**ML 基準、PyTorch trace 與瓶頸分析**。五日驗收全部通過，且能獨立修改小輸入、重新執行與解釋結果，才可進下一週。

實驗報告需有問題、環境、原始資料、正確性、方法、結果與限制。不得要求湊出正向加速；未取得硬體計數器需明列替代證據。第 23 週以原理與診斷設計通關，硬體實測為選修。

[能力成果門檻](../../OUTCOMES.md)｜[官方參考](../../REFERENCES.md)
