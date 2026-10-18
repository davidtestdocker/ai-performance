# 模組 09：伺服器、儲存與訓練資料路徑

[路線](ROADMAP.md)｜目標：查明資料讀取與 checkpoint 是否讓 GPU 等待，理解儲存系統的真實限制。

[觀念講義](CONCEPTS.md)第 09 節｜[作品成果](OUTCOMES.md)

## 學習大綱

伺服器／儲存盤點 → page cache 與 I/O 指標 → 訓練讀取路徑 → checkpoint 停頓與恢復 → 資料放置決策。

## 先理解

檔案系統、block device、page cache、順序／隨機 I/O、同步寫入、共享儲存、物件儲存與 checkpoint。區分磁碟基準的峰值與訓練實際 I/O；不在生產或共享磁碟上做破壞性寫入測試。

## 實作

1. 盤點磁碟或雲端 volume、檔案系統、容量、資料集與 checkpoint 所在位置，量出訓練讀寫量及 CPU/RAM 使用。
2. 在模組 04/05 的固定工作中分段量測資料讀取、預處理、H2D、訓練和 checkpoint；收集 `iostat`、page cache 狀態與 GPU idle。
3. 比較本機資料的冷／熱 cache。若有真正遠端儲存，再對照相同資料版本的遠端路徑；註明網路、儲存、預取與 cache 設定，避免同時改多項。
4. 比較不同 checkpoint 頻率或同步／非同步儲存策略時，確保檔案可成功恢復；報告吞吐、停頓時間、儲存空間與資料安全取捨。

## 做完留下的成果

訓練時間分解、I/O 原始指標、冷／熱 cache 比較、可讀回的 checkpoint，以及一項具體資料放置或 checkpoint 建議。沒有遠端儲存時可完成本機分析，遠端比較保持條件式未測。
