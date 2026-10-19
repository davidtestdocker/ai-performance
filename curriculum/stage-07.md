# 階段 07：分散式系統、儲存與 RDMA

[課綱](ROADMAP.md)｜[進度](../PROGRESS.md)｜[帶練方式](TEACHING.md)

## 要解決的問題

工作變慢時，怎樣區分資源放置、資料路徑、慢 rank 和通訊限制？

前置：階段 03、05；訓練基準已穩定。

## 必要觀念

Slurm 配資源，torchrun 啟動程序。CPU Gloo 驗證程序／collective 語意。DDP 同步梯度；FSDP 切分狀態並交換所需資料。RDMA 需要相容設備與完整路徑。

## 逐步練習

以下按多次教學進行，每次只取一個操作，先講清楚再等待結果。未確認環境前不預寫安裝或訓練命令。

1. 同一張 GPU、同一負載，比較環境允許的 1／2／4 CPU 配額與 binding；核對實際可用集合，分開排隊、啟動與穩態。
2. 量 checkpoint 序列化、寫入及訓練 stall，驗證可載入恢復；比較冷／熱 cache 時記清條件，不任意清系統 cache。
3. 有真實遠端來源才做同資料本機／遠端對照；記網路、檔案系統與 I/O。
4. 同區域兩主機做 TCP 單流／多流，對齊吞吐、RTT、重傳與 CPU；loopback 不代替跨主機。
5. torchrun 啟動兩個 CPU Gloo rank，核對 all_reduce／broadcast；用相同全域 batch 比較單程序與 DDP 更新，控制隨機因素及容忍度。
6. 用自己的模型估算 DDP／FSDP 狀態與通訊，畫同步點、慢 rank 及重疊；公式列假設，不把 CPU 時間代入 NCCL。
7. 逐步學 memory registration、QP、CQ、Send/Recv、Read/Write；盤點設備，再設計 RDMA smoke test、延遲／頻寬、NIC 錯誤及 PFC／ECN／CNP 診斷。
8. 若有多 GPU／RDMA 硬體才執行對應測試；列出 GPU／NIC 拓撲、版本、collective size、擴展率口徑與故障排查順序。

## 可驗收成果

單卡系統調校案例、真實雙主機 TCP、Gloo／DDP 正確性、多卡資料路徑及 RDMA 診斷方案；每項明示已測或需設備。

每個實驗保存目的與假設、環境／輸入、命令、正確性、原始數據、圖與判讀。調整採用或放棄都需理由；用小變化驗證可獨立理解。

## 面試練習

GPU 等 collective 是網路壞了嗎？如何找慢 rank？TCP 量測哪些能協助設計 RDMA 測試、哪些不能外推？

## 目前狀態

未開始。尚無本版實測結果。
