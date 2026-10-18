# 模組 01：Linux 與效能量測方法

[路線](ROADMAP.md)｜目標：判斷數字是否可信，能從 CPU、記憶體、I/O 與 GPU 指標提出可驗證的瓶頸假設。

[觀念講義](CONCEPTS.md)第 01 節｜[作品成果](OUTCOMES.md)

## 本模組使用的機器

這個模組要分辨程式真的慢在哪裡，還是量測方式讓數字失真。
效能工程面試與實務分析都需要先說清楚數字來自哪台機器、使用什麼資源，最後交付可核對的計時與瓶頸判讀。

本專案的「控制節點」是台灣的 VM `instance-20260923-104239`，工作樹位於 `/root/ai-performance`；目前的 CPU 與記憶體盤點由這台 VM 的終端機執行。
之後需要 GPU 計時時，才使用東京的 `compute-gpu01`（規劃配備一張 NVIDIA L4）；它是另一台 VM，不能把控制節點的 CPU 結果當作 GPU VM 的環境資料。
兩台機器的用途與先前查得的資源狀態見[現有機器安排](INFRASTRUCTURE.md)，實驗時仍須核對當下狀態。

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

## 環境盤點：CPU 拓撲

**目的與影響：**在目前的控制節點 VM 查看作業系統所見的 CPU 架構、邏輯 CPU 數、每核心執行緒數與 NUMA 節點數，作為後續 CPU 量測的環境背景。這是唯讀查詢，不建立或修改檔案、服務及雲端資源；VM 內看到的拓撲不等於實體主機全貌。

`lscpu` 是 Linux 查看 CPU 拓撲的工具；在控制節點 VM 執行，讀取系統資訊，不會改動設定。

**已執行指令（在控制節點 VM）：**

```bash
lscpu
```

**實際結果（與判讀有關的欄位）：**

```text
Architecture:                x86_64
CPU(s):                      2
  On-line CPU(s) list:       0,1
  Model name:                Intel(R) Xeon(R) CPU @ 2.20GHz
    Thread(s) per core:      2
    Core(s) per socket:      1
    Socket(s):               1
  Hypervisor vendor:         KVM
  Virtualization type:       full
  NUMA node(s):              1
  NUMA node0 CPU(s):         0,1
```

**判讀：**`CPU(s): 2` 是這台 VM 可用的兩個邏輯 CPU（編號 0、1）；VM 呈現為一個核心、每核心兩個執行緒，並且只有一個 NUMA 節點。
這些是客體 VM 的拓撲，不能推定實體主機只有一個核心，也不能把兩個邏輯 CPU 當作兩個獨立實體核心。

## 環境盤點：記憶體容量

**目的與影響：**在同一台控制節點 VM 查看總記憶體與目前可用量，作為稍後解讀記憶體壓力的起點。`free` 讀取 Linux 的記憶體統計；`-h` 以易讀單位顯示。這是唯讀查詢，不建立或修改檔案、服務及雲端資源。重點看 `total` 與 `available`，後者是系統估計目前可供新工作使用的容量。

**待執行指令（在控制節點 VM）：**

```bash
free -h
```
