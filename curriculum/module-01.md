# 模組 01：Linux 與效能量測方法

[路線](ROADMAP.md)｜目標：判斷數字是否可信，能從 CPU、記憶體、I/O 與 GPU 指標提出可驗證的瓶頸假設。

[觀念講義](CONCEPTS.md)第 01 節｜[作品成果](OUTCOMES.md)

## 學習大綱

量測單位與指標 → Linux/硬體拓撲盤點 → CPU/GPU 正確計時 → 三類瓶頸的系統觀察 → 寫出可被推翻的診斷。

## 先理解

區分延遲、吞吐、利用率、頻寬、峰值顯存、端到端時間與 kernel 時間；理解暖機、CUDA 非同步、page cache、時鐘變動和共用資源如何污染結果。畫出一個訓練 step 的 CPU 資料準備 → H2D → GPU 前反向 → optimizer → checkpoint 路徑。

## 實作順序

1. 盤點 `lscpu`、NUMA、記憶體、磁碟、網卡、GPU、驅動與 CUDA；用 `nvidia-smi` 記錄 GPU 型號、顯存、時脈、功率、溫度與錯誤狀態，可用時再用 DCGM 收集健康／profiling 欄位。記下無法讀取的項目，不補猜值。[NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/health-monitoring.html)
2. 用可核對答案的小型 CPU 工作測量 wall time 與 CPU time；再用 GPU 工作比較未同步主機計時、同步主機計時和 CUDA event，說明差異。[PyTorch CUDA 計時](https://docs.pytorch.org/docs/stable/notes/cuda.html)
3. 對 CPU 密集、記憶體密集和 I/O 密集的簡單工作各做一次觀察，收集 `pidstat`、`iostat`、`vmstat`、`perf stat`（權限允許時）與 GPU 記憶體／活動。不要把 GPU utilization 單一數字直接當成吞吐。[Linux workload tracing](https://docs.kernel.org/admin-guide/workload-tracing.html)
4. 對每個工作先預測瓶頸，再寫出哪一個觀察能推翻預測。

## 做完留下的成果

有一份含 GPU 健康／時脈條件的環境快照、三種工作負載的原始時間與系統指標，以及一頁「數字可信度」報告；能解釋同步前後計時為何不同，並指出至少一個量測陷阱。資料與報告歸入 `results/01/`、`reports/01.md`，未實作前不預建假結果。
