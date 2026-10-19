# W01D01｜CPU 拓樸與虛擬化：實作證據

- 日期：2026-10-19
- 主機提示符：`root@instance-20260923-104239`（Google Cloud Linux VM）
- 目前結果：微步驟 1 通過；微步驟 2 尚待驗證；**整日未通過**
- 指令：`lscpu`

## 微步驟 1：客體 CPU 拓樸

下列為使用者貼回的 `lscpu` 輸出中與課程相關的**原始欄位摘錄**，不是整份原始輸出（其他 CPU flags、漏洞資訊未收錄）：

```text
Architecture:                x86_64
CPU(s):                      2
  On-line CPU(s) list:       0,1
Vendor ID:                   GenuineIntel
  BIOS Vendor ID:            Google
  Model name:                Intel(R) Xeon(R) CPU @ 2.20GHz
    Thread(s) per core:      2
    Core(s) per socket:      1
    Socket(s):               1
Virtualization features:
  Hypervisor vendor:         KVM
  Virtualization type:       full
Caches (sum of all):
  L1d:                       32 KiB (1 instance)
  L1i:                       32 KiB (1 instance)
  L2:                        256 KiB (1 instance)
  L3:                        55 MiB (1 instance)
NUMA:
  NUMA node(s):              1
  NUMA node0 CPU(s):         0,1
```

### 判讀

- Linux 客體可見 2 個邏輯 CPU、1 socket、1 core/socket、2 threads/core。
- KVM VM 的客體拓樸不等於宿主實體拓樸，不能推定有 2 個獨占實體核心，亦不能保證雙倍效能。
- Linux 可見一個 NUMA 節點；客體回報的快取資訊不保證獨占快取。
- 本步只盤點，沒有 CPU 效能實測；Google Cloud 具體機型尚待核對。

### 理解驗收

問題：`CPU(s): 2`、`Thread(s) per core: 2`、`Core(s) per socket: 1` 是否能證明兩個獨占的宿主實體核心？

- 學員選擇：**B** —— Linux 看見兩個邏輯 CPU，但無法確定宿主機實體核心的獨占情況。
- 判定：**正確；微步驟 1 通過**（2026-10-19）。

## 下一步

微步驟 2：執行 `cat /proc/cpuinfo`，比較 `processor`、`physical id`、`core id` 等欄位。尚未取得輸出，不得標記通過。
