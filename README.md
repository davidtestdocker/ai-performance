# HPC AI 效能工程：從頭開始

依鴻海「HPC AI 效能工程師（新北／高雄）」職缺規劃，核心是測試自動化與數據分析、ML 效能分析、LLM 訓練效能分析、分散式系統軟硬體調校。最多一張 GPU，以可核對的程式與實測證據學習 C／C++、Python、Linux、GPU 與 RDMA 診斷。

本版取代舊十二模組，所有新階段從未開始計算；既有 SRE／Kubernetes／GKE／Slurm 經驗用於理解系統問題，不預設已掌握 ML。沒有固定週數、截止日或預填加速比例。

## 從哪裡開始

先讀 [進度](PROGRESS.md)，再從 [階段 00](curriculum/stage-00.md) 的第一步開始。一次只做一個操作，先解釋必要觀念與影響，收到輸出並判讀後再前進。各階段文件會逐步累積真實指令、結果與解釋，不一次貼完整答案程式要求照做。

[課綱與依賴](curriculum/ROADMAP.md)｜[教學方式](curriculum/TEACHING.md)｜[設備安排](curriculum/INFRASTRUCTURE.md)｜[工具取捨](curriculum/TOOL_SELECTION.md)｜[觀念入口](curriculum/CONCEPTS.md)｜[職缺驗收](curriculum/OUTCOMES.md)

## 九階段

- [00 可信量測與系統觀察](curriculum/stage-00.md)
- [01 從零理解一次訓練](curriculum/stage-01.md)
- [02 逐步建立 Python 量測工具](curriculum/stage-02.md)
- [03 ML 訓練管線瓶頸診斷](curriculum/stage-03.md)
- [04 C／C++ 與 CUDA 資料移動](curriculum/stage-04.md)
- [05 LLM 真正訓練與可信基準](curriculum/stage-05.md)
- [06 LLM 訓練效能調校](curriculum/stage-06.md)
- [07 分散式系統、儲存與 RDMA](curriculum/stage-07.md)
- [08 乾淨重現與面試交付](curriculum/stage-08.md)

## 四個成果入口

1. Python 自動化量測：可信計時、原始資料、重跑、錯誤分類、受控比較。
2. ML 診斷：真實資料管線、CPU／GPU timeline、兩輪有證據的調整。
3. LLM 訓練：可控模型與真實模型、有效 token 吞吐、顯存、品質與三份調校實驗。
4. 分散式系統：單卡資源／儲存調校、雙主機 TCP、CPU Gloo／DDP 正確性、多卡與 RDMA 診斷設計。

程式與輸入放在 `project/stage-XX/`，完成實作後才建立；原始結果與 trace 按大小採檔案或具版本／校驗值的外部位置保存，不將權重、資料集、密鑰提交 Git。圖表必須能從原始資料生成。既有 `project/01/` 是舊程式，與新階段 01 不同。

## 舊成果與證據

舊課綱由 Git 歷史保存，不再作現行教學入口。[重排前的量測紀錄](https://github.com/davidtestdocker/ai-performance/blob/e9640f59ee76fa1adcef06750e23ff42e879ff51/curriculum/module-01.md)與既有程式保留作歷史參考，不自動算入新進度。舊熱擴散總和 PASS 只是合理性檢查，新課程會補逐元素參考驗證。

## 硬體與經歷邊界

一張 GPU 可實測單卡訓練與 kernel；CPU Gloo 不能證明 NCCL 擴展率。多 GPU、硬體 RDMA、NVLink、GPUDirect 必須有相應設備與路徑才能宣稱實測。沒有設備可完成診斷設計，狀態標示待硬體；不阻擋其他成果。企業規模經驗與工作年資由真實經歷證明。
