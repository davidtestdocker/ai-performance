# 第 21 週：CPU Gloo 與跨節點 DDP

[固定課綱](../../ROADMAP.md)｜[進度](../../../PROGRESS.md)｜[帶練規則](../../TEACHING.md)

**固定目標：** 從 process group 到真實雙節點訓練，驗證梯度同步與資料切分。

**職缺對應：** D 分散式軟硬體調校；A 可信量測

**設備：** 兩台 CPU VM；PyTorch CPU/Gloo

**先備：** 前 20 週必要驗收通過；新工具仍從最小例子開始。

| 日 | 主題 | 可觀察驗收 |
|---|---|---|
| [D01](day-01/README.md) | Rendezvous 與 process group | 兩台輸出相互對應，endpoint 僅允許測試節點，不能用 localhost 跨機連線。 |
| [D02](day-02/README.md) | Collective 正確性 | 結果數值正確，知道何時除以 world_size，不對單 rank 跳過 collective。 |
| [D03](day-03/README.md) | DDP 梯度與等價更新 | 參數在 ranks 間一致且與 reference 容差相符，loss 正規化正確。 |
| [D04](day-04/README.md) | Sampler 與訓練迴圈 | 清楚標記 padding/drop_last 行為，兩節點步數一致，不雙重 shuffle。 |
| [D05](day-05/README.md) | DDP 除錯與驗收 | 有真實跨機 loss/更新證據、吞吐與失敗診斷，慢 rank 影響被解釋，不要求加速。 |

## 本週成果與通關

必交：**跨節點 DDP 正確性、吞吐與除錯報告**。五日驗收全部通過，且能獨立修改小輸入、重新執行與解釋結果，才可進下一週。

實驗報告需有問題、環境、原始資料、正確性、方法、結果與限制。不得要求湊出正向加速；未取得硬體計數器需明列替代證據。第 23 週以原理與診斷設計通關，硬體實測為選修。

[能力成果門檻](../../OUTCOMES.md)｜[官方參考](../../REFERENCES.md)
