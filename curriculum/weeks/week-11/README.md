# 第 11 週：PyTorch 與神經網路從零

[固定課綱](../../ROADMAP.md)｜[進度](../../../PROGRESS.md)｜[帶練規則](../../TEACHING.md)

**固定目標：** 親寫 tensor、autograd、Module 與完整訓練/驗證流程。

**職缺對應：** B ML 效能分析；A 可信量測

**設備：** CPU 起步，再使用單 GPU

**先備：** 前 10 週必要驗收通過；新工具仍從最小例子開始。

| 日 | 主題 | 可觀察驗收 |
|---|---|---|
| [D01](day-01/README.md) | Tensor、dtype 與 device | 能列每個 tensor 的三項屬性，錯誤 device 問題能定位。 |
| [D02](day-02/README.md) | Autograd | 梯度與 NumPy reference 相符，能解釋清零時機與 leaf tensor。 |
| [D03](day-03/README.md) | Module 與 MLP | 參數量與程式一致，子模組正確註冊且 optimizer 能看到所有參數。 |
| [D04](day-04/README.md) | Dataset、DataLoader 與 optimizer | 參數確實更新，小樣本 loss 有下降；能解釋 shuffle、batch 與最後不足 batch。 |
| [D05](day-05/README.md) | 驗證、Checkpoint 與重現 | 恢復後 step 與參數合理一致，保存版本與容差；不將權重提交 Git。 |

## 本週成果與通關

必交：**可在 CPU/GPU 訓練的 MLP 與 checkpoint**。五日驗收全部通過，且能獨立修改小輸入、重新執行與解釋結果，才可進下一週。

實驗報告需有問題、環境、原始資料、正確性、方法、結果與限制。不得要求湊出正向加速；未取得硬體計數器需明列替代證據。第 23 週以原理與診斷設計通關，硬體實測為選修。

[能力成果門檻](../../OUTCOMES.md)｜[官方參考](../../REFERENCES.md)
