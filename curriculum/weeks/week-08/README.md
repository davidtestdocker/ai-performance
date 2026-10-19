# 第 08 週：CUDA 記憶體與 kernel 調校

[固定課綱](../../ROADMAP.md)｜[進度](../../../PROGRESS.md)｜[帶練規則](../../TEACHING.md)

**固定目標：** 以正確性與量測支持 coalescing、shared memory 與 reduction 設計。

**職缺對應：** B ML 效能分析；C LLM 訓練效能分析的 GPU 基礎

**設備：** 一張 NVIDIA GPU

**先備：** 前 07 週必要驗收通過；新工具仍從最小例子開始。

| 日 | 主題 | 可觀察驗收 |
|---|---|---|
| [D01](day-01/README.md) | CUDA events 計時 | 報告 kernel_ms 與 end_to_end_ms，暖機與重複次數明列。 |
| [D02](day-02/README.md) | Coalescing 與有效頻寬 | 兩版本語意和工作量相同，明寫 bytes 計算，不宣稱等於實測 DRAM traffic。 |
| [D03](day-03/README.md) | Shared memory 與同步 | 逐元素驗證且無 deadlock，畫出 tile 的載入與寫回索引。 |
| [D04](day-04/README.md) | Parallel reduction | 正確處理尾端、初始值與多 block，誤差標準有依據。 |
| [D05](day-05/README.md) | Launch 配置與資源取捨 | 至少三個合法配置、重複五次，最佳配置需有穩定證據，非只挑單次最小值。 |

## 本週成果與通關

必交：**三個 CUDA A/B 實驗與可重現基準**。五日驗收全部通過，且能獨立修改小輸入、重新執行與解釋結果，才可進下一週。

實驗報告需有問題、環境、原始資料、正確性、方法、結果與限制。不得要求湊出正向加速；未取得硬體計數器需明列替代證據。第 23 週以原理與診斷設計通關，硬體實測為選修。

[能力成果門檻](../../OUTCOMES.md)｜[官方參考](../../REFERENCES.md)
