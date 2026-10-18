# 模組 05：LLM 訓練工作負載與基準

[路線](ROADMAP.md)｜目標：先讓 LLM 真正訓練且結果可信，再討論調校。

[觀念講義](CONCEPTS.md)第 05 節｜[作品成果](OUTCOMES.md)

## 學習大綱

decoder-only 訓練與顯存 → 小模型正確性 → 開源模型與資料版本 → full fine-tuning/LoRA 邊界 → tokens/s 與 step 分段基準。

## 先理解

decoder-only 模型的 attention、MLP、tokenization、padding、序列長度、microbatch、gradient accumulation、optimizer state 與 activation 顯存。分清預訓練、全參數微調、LoRA 和推論；它們的訓練成本不能互換。[Transformers 單 GPU 訓練指南](https://huggingface.co/docs/transformers/main/perf_train_gpu_one)

## 實作順序

1. 做可設定層數、hidden size、序列長度的小型 decoder-only 模型；用固定 token 資料跑前向、反向和 optimizer，驗證 loss 有限、梯度非空、參數確實更新。
2. 選單卡能承受、授權清楚的開源預訓練 causal LM 與固定資料集；記錄 checkpoint revision、tokenizer、資料版本。依顯存選 full fine-tuning 或 LoRA，不能把 LoRA 當全參數結果。[PEFT LoRA](https://huggingface.co/docs/peft/main/package_reference/lora)
3. 用模組 02 平台量測 non-padding training tokens/s、step 延遲、峰值已分配／保留顯存、optimizer 更新率、loss 與錯誤。記錄 microbatch × accumulation 的有效 batch 與序列長度分布。
4. 用 Profiler 分開資料、前向、反向、optimizer；保存可開啟 trace，找出下一模組的調校題目。

## 做完留下的成果

兩層工作負載均有可重跑命令和基準數據；至少一個真實模型完成有效訓練更新；正確性與顯存使用有證據；報告能解釋為何所選模型與序列長度適合這張 GPU。
