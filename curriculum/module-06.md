# 模組 06：LLM 訓練效能調校

[路線](ROADMAP.md)｜目標：用 profile 指導實驗，回答吞吐、顯存和訓練有效性之間的取捨。

[觀念講義](CONCEPTS.md)第 06 節｜[作品成果](OUTCOMES.md)

## 學習大綱

從 trace 提假設 → 控制有效 batch 的 A/B → 精度／checkpoint／attention 路徑 → 瓶頸轉移 → 反例與最佳已測設定。

## 先理解

比較前先固定工作量與有效 batch。理解 mixed precision、activation checkpointing、SDPA backend、padding、optimizer 對時間與記憶體的不同影響；配置名稱不等於實際 backend 已啟用。[PyTorch checkpointing](https://docs.pytorch.org/docs/stable/checkpoint)、[PyTorch SDPA](https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html)

## 實作順序

1. 從模組 05 trace 寫出至少三個可推翻的假設：例如 attention 時間過高、microbatch 太小、activation 顯存限制、資料處理造成 GPU 空檔。
2. 每個假設只調一個主要變因；做相同環境的 A/B 重複量測，核對實際 backend、非 padding tokens/s、step 分布、峰值顯存、loss／梯度和失敗率。
3. 至少一輪比較速度／顯存取捨，例如 checkpointing 換取較大 batch；至少保留一輪無效或反效果實驗並解釋原因。
4. 把最優的**已測設定**和適用範圍寫成工程建議；另一張 GPU 或不同模型只能重新驗證，不能直接沿用數字。

## 做完留下的成果

三份完整實驗卡（假設、控制變因、trace、原始資料、判斷），一份總報告和重現命令。能回答「瓶頸是否轉移」及「改善吞吐付出了什麼代價」。不要求一定取得正向提升。
