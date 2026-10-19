# 第 14 週：LLM 基礎與 Attention 實作

[固定課綱](../../ROADMAP.md)｜[進度](../../../PROGRESS.md)｜[帶練規則](../../TEACHING.md)

**固定目標：** 從 token 與機率開始親寫 causal attention，不預設 NLP 知識。

**職缺對應：** C LLM 訓練效能分析；A 可信量測

**設備：** CPU 起步，單 GPU 驗證

**先備：** 前 13 週必要驗收通過；新工具仍從最小例子開始。

| 日 | 主題 | 可觀察驗收 |
|---|---|---|
| [D01](day-01/README.md) | Token 與序列資料 | 未知字元策略明確、無驗證集洩漏，保存文本來源與雜湊。 |
| [D02](day-02/README.md) | Embedding 與位置 | 能指出參數量 V×D，超過 context 長度有明確錯誤。 |
| [D03](day-03/README.md) | Softmax 與交叉熵 | 極大 logits 不溢位，機率和接近 1，梯度有限。 |
| [D04](day-04/README.md) | QKV 與 scaled attention | 與小型 reference 相符，能解釋 transpose 位置與 T×T 記憶體。 |
| [D05](day-05/README.md) | Causal mask 與多頭 | 未來資訊不可洩漏，head 維度可整除，mask dtype/方向正確。 |

## 本週成果與通關

必交：**tokenizer、小型 attention 與形狀測試**。五日驗收全部通過，且能獨立修改小輸入、重新執行與解釋結果，才可進下一週。

實驗報告需有問題、環境、原始資料、正確性、方法、結果與限制。不得要求湊出正向加速；未取得硬體計數器需明列替代證據。第 23 週以原理與診斷設計通關，硬體實測為選修。

[能力成果門檻](../../OUTCOMES.md)｜[官方參考](../../REFERENCES.md)
