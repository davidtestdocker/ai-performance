# 模組 02：測試自動化、統計與資料庫

[路線](ROADMAP.md)｜目標：建立後續模組共用的 `perfctl`，讓另一個人能重跑、檢查與比較結果。

[觀念講義](CONCEPTS.md)第 02 節｜[作品成果](OUTCOMES.md)

## 學習大綱

實驗設計與樣本 → CLI/資料 schema → 執行與故障處理 → 統計比較 → SQLite 索引與查詢 → 重現性審查。

## 先理解

實驗單位、獨立重複、暖機、控制變因、失敗樣本、P95 的樣本數、版本漂移；區分原始事件資料與可查詢索引。認識 SQLite transaction、index、WAL 的使用條件。[SQLite WAL](https://www.sqlite.org/wal.html)

## 實作順序

1. 定義 YAML 工作矩陣與輸出 schema：命令、參數、環境、模型／資料版本、開始／結束時間、退出碼、每個 step、loss／品質指標、錯誤和資源指標。若只量固定步數吞吐，明確標示它不同於訓練到目標品質的時間；參照 MLPerf Training 的公平比較與資訊揭露方法，但不宣稱正式 MLPerf 成績。[MLCommons Training](https://mlcommons.org/benchmarks/training/)
2. 用 Python 實作預檢、逾時、暖機、重複執行與中斷後保留資料。先在 CPU 跑，再接 GPU；所有執行輸出 JSONL。
3. 加入比較器：只比較相同硬體、模型、資料、精度和有效 batch；報中位數、分散度、樣本數、失敗率及差異。P95 需有足夠的逐步樣本。
4. 用 SQLite 索引 run、environment、metric；比較有無 index 的真實查詢與 `EXPLAIN QUERY PLAN`。跨主機資料由單一收集器匯入，SQLite WAL 不放網路檔案系統上。[SQLite 查詢計畫](https://www.sqlite.org/eqp.html)
5. 設計一個錯誤參數、一次 OOM/逾時和一次環境版本不一致，確認它們不被納入有效改善。

## 做完留下的成果

同一規格一條命令可重跑；從 JSONL 能獨立重算報告；失敗樣本與版本差異可見；SQLite 查詢有前後證據。提交 CLI 說明、樣本規格、原始數據、比較圖與設計取捨。統計結果不需事先達到指定改善百分比。
