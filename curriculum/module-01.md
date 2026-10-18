# 模組 01：Linux 與效能量測方法

[路線](ROADMAP.md)｜目標：判斷數字是否可信，能從 CPU、記憶體、I/O 與 GPU 指標提出可驗證的瓶頸假設。

[觀念講義](CONCEPTS.md)第 01 節｜[作品成果](OUTCOMES.md)

## 本模組使用的機器

這個模組要分辨程式真的慢在哪裡，還是量測方式讓數字失真。
效能工程面試與實務分析都需要先說清楚數字來自哪台機器、使用什麼資源，最後交付可核對的計時與瓶頸判讀。

本專案的「控制節點」是台灣的 VM `instance-20260923-104239`，工作樹位於 `/root/ai-performance`；目前的 CPU 與記憶體盤點由這台 VM 的終端機執行。
之後需要 GPU 計時時，使用東京的 `compute-gpu01`（規劃配備一張 NVIDIA L4）。
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

**目的與影響：**在目前的控制節點 VM 查看作業系統所見的 CPU 架構、邏輯 CPU 數、每核心執行緒數與 NUMA 節點數，作為後續 CPU 量測的環境背景。這是唯讀查詢，不建立或修改檔案、服務及雲端資源。

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

**判讀：**

| 欄位 | 看到的值 | 代表什麼 |
|---|---|---|
| `CPU(s)`、`On-line CPU(s) list` | `2`、`0,1` | 這台 VM 目前可用兩個邏輯 CPU，編號為 0 和 1。邏輯 CPU 是作業系統可排程的一個執行位置。 |
| `Thread(s) per core` | `2` | 在 VM 顯示的拓撲中，一個核心提供兩個邏輯執行緒。 |
| `Core(s) per socket`、`Socket(s)` | `1`、`1` | VM 顯示為一個 socket、其中一個核心；配合上一列，得到兩個邏輯 CPU。 |
| `NUMA node(s)` | `1` | VM 顯示一個 NUMA 節點。 |
| `Hypervisor vendor` | `KVM` | 這台機器使用 KVM 虛擬化。 |

## 環境盤點：記憶體容量

**目的與影響：**在同一台控制節點 VM 查看總記憶體與目前可用量，作為稍後解讀記憶體壓力的起點。`free` 讀取 Linux 的記憶體統計；`-h` 以易讀單位顯示。這是唯讀查詢，不建立或修改檔案、服務及雲端資源。重點看 `total` 與 `available`，後者是系統估計目前可供新工作使用的容量。

**已執行指令（在控制節點 VM）：**

```bash
free -h
```

**實際結果：**

```text
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       1.4Gi       1.8Gi        16Mi       786Mi       2.4Gi
Swap:             0B          0B          0B
```

**判讀：**

| 欄位 | 看到的值 | 代表什麼 |
|---|---|---|
| `Mem: total` | `3.8Gi` | VM 目前可見的記憶體總量。 |
| `Mem: used` | `1.4Gi` | 目前計入使用中的記憶體；不能只看這欄判定是否缺記憶體。 |
| `Mem: free` | `1.8Gi` | 當下完全空閒的記憶體。 |
| `Mem: buff/cache` | `786Mi` | Linux 用於緩衝與快取的記憶體，其中一部分可在程式需要時回收。 |
| `Mem: available` | `2.4Gi` | 系統估計可供新工作使用的容量，包含可回收的部分；這是估計值，不是保證可分配的上限。 |
| `Swap: total` | `0B` | 這台 VM 沒有設定 swap。 |

`available` 比 `free` 大，是因為系統估計部分緩衝與快取可以回收。

## 環境盤點：磁碟與掛載點

`lsblk` 會列出 Linux 看見的磁碟與分割區。這裡用它確認控制節點有哪些磁碟、容量多大，以及各分割區掛載到哪個目錄；之後量測檔案 I/O 時才知道實際使用的磁碟位置。

**目的與影響：**在控制節點 VM 查詢磁碟清單。`-o` 指定只顯示名稱、類型、容量、型號與掛載點；指令只讀取資訊，不建立或修改檔案、服務及雲端資源。

**已執行指令（在控制節點 VM）：**

```bash
lsblk -o NAME,TYPE,SIZE,MODEL,MOUNTPOINTS
```

**實際結果：**

```text
NAME   TYPE  SIZE MODEL          MOUNTPOINTS
sda    disk  100G PersistentDisk
sdb    disk   10G PersistentDisk
├─sdb1 part  200M                /boot/efi
└─sdb2 part  9.8G                /
```

**判讀：**

| 重點欄位 | 結果 | 意義 |
|---|---|---|
| `sdb2` 的 `MOUNTPOINTS` | `/` | 根目錄位於 9.8G 的 `sdb2` 分割區；目前工作樹也位於這個檔案系統。 |
| `sda` 的 `SIZE`、`MOUNTPOINTS` | `100G`、空白 | 系統看得到這顆 100G 磁碟，但它目前沒有掛載點。 |

## 環境盤點：根目錄可用空間

`lsblk` 顯示磁碟與分割區大小；`df` 用來查看檔案系統目前的已用與可用空間。這裡只查工作樹所在的根目錄 `/`。

**目的與影響：**在控制節點 VM 讀取 `/` 的容量統計；`-h` 以易讀單位顯示。這是唯讀查詢，不修改檔案或服務。

**已執行指令（在控制節點 VM）：**

```bash
df -h /
```

**實際結果：**

```text
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdb2       9.8G  8.0G  1.8G  82% /
```

**判讀：**`/` 位於 `/dev/sdb2`，總容量 9.8G，已用 8.0G，還有 1.8G 可用。

## 環境盤點：網路介面

`ip` 是 Linux 查看網路狀態的工具。這裡先看控制節點有哪些介面及 IP 位址，記下目前操作的是哪台機器的網路環境。

**目的與影響：**在控制節點 VM 讀取介面名稱、狀態與 IP 位址。`-br` 用簡短格式顯示，`addr` 指定查看位址；這是唯讀查詢，不修改網路設定或服務。

**已執行指令（在控制節點 VM）：**

```bash
ip -br addr
```

**實際結果：**

```text
lo               UNKNOWN        127.0.0.1/8 ::1/128
eth0             UP             10.140.0.2/32 fe80::2725:28ff:b62c:9e10/64
```

**判讀：**

| 介面 | 重點結果 | 意義 |
|---|---|---|
| `lo` | `127.0.0.1/8` | 本機回送介面。 |
| `eth0` | `UP`、`10.140.0.2/32` | 控制節點目前啟用的網路介面及其 IPv4 位址。 |

## CPU 計時：確認 Python

下一段會用 Python 程式量測同一份 CPU 工作的 wall time 與 CPU time。先確認控制節點 VM 可用的 Python 版本，之後在結果中記錄實際使用的版本。

**目的與影響：**`python3 --version` 只查詢版本，不建立或修改檔案、服務及雲端資源。

**已執行指令（在控制節點 VM）：**

```bash
python3 --version
```

**實際結果：**

```text
Python 3.12.15
```

**判讀：**控制節點接下來使用 Python 3.12.15 執行 CPU 計時程式。

## CPU 計時：wall time 與 CPU time

wall time 是從開始到完成實際經過的時間；CPU time 是程式在 CPU 上執行所累積的時間。
在控制節點執行[計時程式](../project/01/cpu_timing.py)：它先計算 `0` 到 `4,999,999` 的平方和，與公式答案核對，再量這段工作的 wall time 與 CPU time；接著等待半秒，量同樣兩個時間作對照。
程式只使用 Python 標準函式庫，不讀寫檔案或修改服務。

**已執行指令（在控制節點 VM 的 `/root/ai-performance`）：**

```bash
python3 project/01/cpu_timing.py
```

**實際結果：**

```text
平方和正確：41666654166667500000
CPU 計算：wall=0.462751s cpu=0.457627s
等待半秒：wall=0.500201s cpu=0.000059s
```

**判讀：**平方和與公式答案一致，計算工作正確完成。

| 工作 | wall time | CPU time | 意義 |
|---|---:|---:|---|
| 計算 500 萬項平方和 | 0.462751 秒 | 0.457627 秒 | 程式大部分經過時間都在使用 CPU。 |
| 等待半秒 | 0.500201 秒 | 0.000059 秒 | 等待算入經過時間，幾乎不消耗 CPU 計算時間。 |

**第二次執行同一指令的實際結果：**

```text
平方和正確：41666654166667500000
CPU 計算：wall=0.484902s cpu=0.470027s
等待半秒：wall=0.500145s cpu=0.000047s
```

| CPU 計算 | 第一次 | 第二次 | 差值 |
|---|---:|---:|---:|
| wall time | 0.462751 秒 | 0.484902 秒 | 第二次多 0.022151 秒 |
| CPU time | 0.457627 秒 | 0.470027 秒 | 第二次多 0.012400 秒 |

兩次等待段的 wall time 都約 0.5 秒、CPU time 都接近 0；相同程式的 CPU 計算時間則有小幅變動。

## 系統指標：先看控制節點狀態

`vmstat` 會同時顯示 CPU 使用情形、記憶體與工作排隊等系統指標。先在沒有刻意啟動測試工作時取得輸出，作為接下來觀察 CPU 工作時的對照。

**目的與影響：**在控制節點 VM 查看統計；指令只讀取資訊，不修改檔案或服務。`vmstat 1 4` 中的 `1` 是秒數間隔，`4` 是輸出筆數。第一筆是自開機以來的平均值；後三筆各代表前一秒的情形，用後三筆看目前狀態。

**待執行指令（在控制節點 VM）：**

```bash
vmstat 1 4
```
