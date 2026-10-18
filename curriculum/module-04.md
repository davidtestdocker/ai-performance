# 模組 04：ML 訓練管線效能

[路線](ROADMAP.md)｜目標：定位真實 ML 訓練中的資料供給、CPU、H2D 與 GPU 算子瓶頸。

[觀念講義](CONCEPTS.md)第 04 節｜[作品成果](OUTCOMES.md)

## 學習大綱

訓練 step 資料路徑 → 真實與合成資料對照 → CPU/GPU profiler → 瓶頸假設 → 兩輪受控調整 → 資源代價與正確性。

## 先理解

Dataset/DataLoader、batch、worker、prefetch、pinned memory、GPU 非同步、前反向與 optimizer；理解合成資料基準的用途與限制。Profiler 先少量採樣，避免把 trace 開銷當作正常吞吐。[PyTorch Profiler](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)

## 實作順序

1. 固定一個小型影像模型和授權清楚的公開資料集；記錄資料版本、切分、batch、精度和正確性／loss。資料先本機化，控制下載抖動。
2. 跑完整訓練與合成資料對照，收集 samples/s、step 分布、CPU/RAM、GPU 顯存與資料等待；用 Profiler 標記載入、H2D、前向、反向和 optimizer。
3. 根據 trace 選兩個瓶頸做調校，例如 worker、prefetch、pinned memory、batch 或資料布局。每次只改主要變因，記錄資源代價和結果。若 trace 顯示非資料瓶頸，不強迫調 DataLoader。[PyTorch 資料載入教學](https://docs.pytorch.org/tutorials/intermediate/intermediate_data_loading_tutorial.html)
4. 如有兩種儲存路徑，再比較本機與遠端資料；把 page cache、檔案系統、磁碟類型和 `iostat` 放進報告。

## 做完留下的成果

保存一份 CPU/GPU timeline、一張 step 時間分解圖、兩輪 A/B 原始數據與接受／放棄調整的理由。能指出合成資料吞吐為何不能代表真實資料吞吐。
