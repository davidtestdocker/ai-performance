# 階段 05：LLM 真正訓練與可信基準

[課綱](ROADMAP.md)｜[進度](../PROGRESS.md)｜[帶練方式](TEACHING.md)

## 要解決的問題

如何量出一張 GPU 的 LLM 訓練能力，並證明數字不是推論或 padding 灌水？

前置：階段 02、03；運用階段 04 的資料移動觀念。

## 必要觀念

先學 token 與 next-token label，再學 embedding、causal mask、attention、MLP。有效 batch＝microbatch×gradient accumulation×資料並行 world size；單卡最後一項為 1。

## 逐步練習

以下按多次教學進行，每次只取一個操作，先講清楚再等待結果。未確認環境前不預寫安裝或訓練命令。

1. 用極小 token 序列手動對齊 input／label，辨識 padding、忽略標籤及有效 loss token。
2. 建立 embedding 與輸出預測，核對張量形狀，再加入 causal attention 與單層 decoder block。
3. 跑完整前反向與 optimizer，驗證梯度、參數更新及小資料 loss。
4. 確認顯存與磁碟後，固定一個授權清楚的小型預訓練 causal LM、tokenizer revision 與資料切分。
5. 優先選能容納的全參數小模型作基準；另做 LoRA 時獨立標記方法及可訓練參數，不混稱結果。
6. 用量測工具收有效訓練 tokens/s、optimizer updates/s、step 時間、峰值 allocated／reserved 顯存、訓練及固定驗證 loss。
7. 匯出短 trace，分辨資料、前向、反向、optimizer，列下一階段可推翻的假設。

## 可驗收成果

可控小模型與真實模型都有有效訓練證據；token 計數口徑清楚；模型、資料、batch、精度、版本與顯存可追溯。

每個實驗保存目的與假設、環境／輸入、命令、正確性、原始數據、圖與判讀。調整採用或放棄都需理由；用小變化驗證可獨立理解。

## 面試練習

LoRA 的數字能代表全參數訓練嗎？改 accumulation 後，tokens/s 與更新率如何一起看？

## 目前狀態

未開始。尚無本版實測結果。
