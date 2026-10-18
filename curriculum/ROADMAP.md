# HPC AI 效能工程：模組學習路線

[作品設計](../README.md)｜[工具選型分析](TOOL_SELECTION.md)｜[技術觀念講義](CONCEPTS.md)｜[作品成果對照](OUTCOMES.md)。依能力相依順序學習，沒有週數、截止日或指令數上限。下列模組數量來自不同的實驗問題與作品成果，帶練時若一個模組太大或前置知識不足，可以再拆。每個模組以「理解觀念 → 寫程式 → 做實驗 → 分析結果 → 留下作品」推進。

| 模組 | 要解決的問題 | 作品結果 | 對應職缺 | 使用技術 |
|---|---|---|---|---|
| [01 Linux 與量測方法](module-01.md) | 看到的慢是 CPU、記憶體、I/O、GPU，還是量測錯誤？ | 正確計時、環境快照、瓶頸假設與反證 | Linux 效能、系統架構 | `lscpu`、`vmstat`、`pidstat`、`iostat`、`perf stat`、`nvidia-smi`／DCGM（可用時）、CUDA Event |
| [02 測試自動化與數據](module-02.md) | 如何批量重跑並可靠比較？ | `perfctl`、失敗處理、JSONL/SQLite、統計報告 | Python、自動化、資料分析、資料庫 | Python CLI、YAML、JSONL、CSV、SQLite、`EXPLAIN QUERY PLAN`；MLPerf Training 公平比較方法 |
| [03 GPU 與 C++/CUDA](module-03.md) | kernel、記憶體傳輸和資料布局如何影響性能？ | 正確性可核對的 microbenchmark 與 profile | GPU、C/C++、系統架構 | C++、CUDA C++、CUDA Event、Nsight Compute |
| [04 ML 訓練管線](module-04.md) | GPU 為何等待資料或算子？ | 真實資料集訓練與兩輪有證據的調校 | ML frameworks、Linux、儲存 | PyTorch `Dataset`／`DataLoader`／Profiler、Nsight Systems、`iostat` |
| [05 LLM 訓練基礎](module-05.md) | 訓練 step 的時間與記憶體去哪裡？ | 可控模型與真實模型微調基準，記錄 loss／品質 | LLM、GPU、ML | PyTorch、Transformers、tokenizer、PEFT/LoRA、CUDA |
| [06 LLM 訓練調校](module-06.md) | 何種設定改善吞吐，代價是什麼？ | 三輪 A/B、profiler trace、顯存／速度／品質取捨 | LLM 訓練效能分析 | PyTorch Profiler、AMP、SDPA、activation checkpointing、`torch.compile`（適用時） |
| [07 TCP 網路效能](module-07.md) | 慢是 RTT、重傳、頻寬還是 CPU？ | 兩主機 TCP 指標、封包與吞吐曲線 | 網路協定、Linux | TCP、`ip`、`ss`、`ethtool`、`iperf3`、`tcpdump`（權限允許時） |
| [08 分散式訓練機制](module-08.md) | rank 同步、DDP／FSDP 資料移動與工作放置如何影響效能？ | Gloo 最小正確性實作、DDP／FSDP／NCCL 路徑圖、多卡故障診斷與待驗證設計；有 Slurm 時加資源與工作內時間分析 | 分散式系統 | `torchrun`、PyTorch `torch.distributed`／Gloo、DDP／FSDP、張量／流水線並行機制、NCCL 診斷；Slurm `sbatch`／`srun`／GRES（可用時） |
| [09 伺服器與儲存](module-09.md) | 資料讀取與 checkpoint 如何拖慢訓練？ | 本機／遠端路徑、page cache、I/O stall 證據 | 伺服器、儲存系統 | Linux 檔案系統、page cache、`iostat`、PyTorch checkpoint、本機／遠端儲存 |
| [10 RDMA 架構與診斷](module-10.md) | TCP 結論哪些不能外推到 RDMA？ | 資料路徑與診斷報告；有硬體才加實測 | RDMA、網路協定 | RDMA verbs、RoCE／InfiniBand、`rdma link`、`ibv_devinfo`、`rping`／perftest（有硬體時） |
| [11 雲端重現](module-11.md) | 換一台機器能否重跑結果？ | GPU 環境部署、版本、成本和複測 | 雲端運算 | Linux VM、容器、GPU driver／CUDA runtime、PyTorch、IaC（採用時） |
| [12 開源貢獻與作品記錄](module-12.md) | 別人能否重現並使用成果？ | 上游貢獻、證據索引、專案文件 | 開源、合作溝通 | Git、上游 issue／PR、Markdown、版本固定與校驗值 |

Slurm 在本路線作為 HPC 工作分配與放置的具體平台；沿用可用的叢集執行效能實驗，不再重建一套叢集。Ray 是有動態 Python 分散式工作流或團隊使用時的延伸，**不列為這份職缺的通用必修**。選型理由與單 GPU 邊界見[工具選型分析](TOOL_SELECTION.md)。

## 帶練方式

1. 先讀當前模組的名詞、目標和實驗設計，寫出預期結果及可能反例。
2. 只執行本模組需要的命令；執行前記錄用途、會修改的檔案或服務。安裝、雲端資源和外部提交依當下授權處理。
3. 每次實驗保存命令、環境版本、原始資料、圖和判讀。若結果與預測相反，調查原因，不改寫假設讓它看起來正確。
4. 完成模組的程式、實驗與結果分析後更新進度。概念學習、程式完成、單機測試與跨節點測試分別標示，不合併聲稱。

## 單 GPU 邊界

單卡足以實測 GPU kernel、ML/LLM 訓練與資料供給。CPU 多節點可以驗證 PyTorch rank／collective 語意，網路性能由模組 07 的真實 TCP 實驗分析；CPU Gloo 延遲不能代替多 GPU NCCL 效能。RDMA、GPU Direct、NVLink、多 GPU 擴展率需要對應硬體。模組 08 學 DDP／FSDP／NCCL 機制與待驗證量測設計，模組 10 學 RDMA 架構與診斷；沒有設備時清楚標記「設計，未實測」。

## 專案證據狀態

本路線目前是規劃。任何「已完成」必須連到可重跑的程式、實際命令、原始結果和判讀。既有 `hpc-arch` 可提供實驗環境，但它的舊結果不能冒充本作品的新量測。
