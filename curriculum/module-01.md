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

## 實際進度與盤點紀錄

**2026-10-18：助理先行執行唯讀盤點。**這不是學習者親自執行的結果，也不是效能實測。當時未保存精確時間、各命令的個別退出碼與完整原始輸出；以下只記錄可核對的命令及輸出摘錄，不據此判定瓶頸。

執行命令：

```bash
hostname; lscpu; free -h; lsblk -o NAME,TYPE,SIZE,MODEL,MOUNTPOINTS; command -v nvidia-smi; command -v numactl
```

整行退出碼為 `1`，最後的 `command -v numactl` 沒有找到指令；個別命令的退出碼未保存。輸出摘錄：

```text
instance-20260923-104239
CPU(s):                                  2
Thread(s) per core:                      2
Core(s) per socket:                      1
Socket(s):                               1
Hypervisor vendor:                       KVM
NUMA node(s):                            1
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       1.5Gi       1.8Gi        16Mi       781Mi       2.3Gi
Swap:             0B          0B          0B
NAME   TYPE  SIZE MODEL          MOUNTPOINTS
sda    disk  100G PersistentDisk
sdb    disk   10G PersistentDisk
├─sdb1 part  200M                /boot/efi
└─sdb2 part  9.8G                /root/ai-performance/.git
                                 /root/ai-performance
                                 /tmp/codex-bwrap-synthetic-mount-targets-0
                                 /tmp
                                 /
```

這台 VM 顯示 2 個邏輯 CPU、1 個 NUMA 節點；`available` 記憶體當時約 2.3 GiB。`command -v nvidia-smi` 沒有輸出，只表示目前 PATH 找不到該指令，不能據此斷定沒有 GPU。`lsblk` 顯示 100G 磁碟沒有掛載點，不能據此判定它沒有資料。以上是 VM 內看到的資訊，不能直接當成實體主機規格。

**下一步由學習者執行：**分別執行 `hostname`、`lscpu`、`free -h`，保留原始輸出與各命令退出碼，再把結果記在本節。之後才進入 CPU 計時。
