# AI 效能作品的現有機器使用安排

[作品設計](../README.md)｜[模組路線](ROADMAP.md)。以下狀態於 2026-10-18 以 GCP 唯讀查詢核對；開始每次實驗前重新查 VM 狀態、磁碟可用空間和實際帳單。這是資源安排，不表示已開機或完成新實測。

| 現有資源 | 2026-10-18 狀態 | 這份作品的用途 | 使用安排 |
|---|---|---|---|
| `instance-20260923-104239`，台灣 `asia-east1-b`，2 vCPU／4 GiB | 運行中；10 GiB 系統磁碟剩約 1.8 GiB | 目前工作樹、輕量 Python／Linux 實驗、必要時的 Slurm 控制端 | 正在此機工作時保持運行；工作結束、成果已保存且不需控制端時可停止。不要把大型模型、資料集或 trace 放在剩餘系統磁碟空間。 |
| `compute-gpu01`，東京 `asia-northeast1-c`，4 vCPU／16 GiB／1 張 NVIDIA L4；40 GiB 開機磁碟 | 已停止 | 模組 01 的 GPU 計時、03–06 單卡訓練與 profiler、08 單卡 Slurm 工作、09 儲存與 11 環境複測 | 需要 GPU 時才啟動，集中完成同一批實驗後停止。開機先量模型／資料／checkpoint／trace 所需空間，再決定是否要加資料磁碟或擴大現有磁碟。 |
| `compute-cpu02`，東京 `asia-northeast1-c`，2 vCPU／8 GiB | 已停止 | 模組 07 與 GPU VM 做同區域兩主機 TCP 實驗；需要時做模組 08 的跨節點 Gloo 啟動 | 只在跨主機實驗窗口啟動，和 GPU VM 同區域量測；完成後停止。它的 Zabbix 舊用途對 AI 效能主線非必要。 |
| `openstack-lab01`，東京 `asia-northeast1-c`，2 vCPU／8 GiB；內有 `compute-cpu01` 客體 | 已停止 | 保留 `hpc-arch` 的 OpenStack／四節點叢集成果 | AI 效能主線不需啟動。只有回頭做 OpenStack 或四節點 Slurm 故障／部署實驗時才啟動。 |

## 按模組啟動

| 模組 | 最小運行組合 | 備註 |
|---|---|---|
| 01–02 | 控制節點；01 的 GPU 計時片段再開 GPU VM | CPU／自動化部分可先做，無須整天開 GPU。 |
| 03–06 | GPU VM；用 Slurm 提交時再開控制節點 | GPU VM 上的本機資料作基線；跨台灣／東京 NFS 不作單卡儲存基線。 |
| 07 | GPU VM ＋ `compute-cpu02` | 兩台都在東京同一 zone；先查實際 IP／路由／網路負載。可安排在 GPU 訓練實驗同一開機窗口。 |
| 08 | CPU Gloo 正確性：一台可跑兩 process；單卡 Slurm：控制節點 ＋ GPU VM；跨主機 Gloo：GPU VM ＋ `compute-cpu02` | 不需要四節點同時運行，也不把 CPU Gloo 時間當 NCCL 效能。 |
| 09 | GPU VM；真實遠端儲存比較時再開提供資料的一台現有 VM | 先做本機資料、page cache、checkpoint；遠端路徑要寫明區域與網路條件。 |
| 10 | 現有一台 Linux VM 做設備盤點與設計 | 現有設備沒有已證實的 RDMA 雙主機路徑；不為此先新增 VM。 |
| 11–12 | 現有 VM 與作品檔案 | 環境重建先用固定容器／環境規格；若需證明全新 VM 部署，可在後期以短暫新 VM 複測，不要求同時存在第二張 GPU。 |

## 是否新增資源

**目前沒有必須新增的 VM。** 先用現有 GPU 與同區域 CPU VM 完成核心實驗。只有實際空間盤點顯示 40 GiB GPU 開機磁碟不足，才考慮 GPU VM 的獨立資料磁碟或擴大既有磁碟；固定模型與資料規模後決定容量，避免先租後猜。GCP 磁碟擴容通常不可直接縮小，變更前先備份並確認費用。[GCP 擴充 Persistent Disk](https://docs.cloud.google.com/compute/docs/disks/resize-persistent-disk)

控制節點另掛一顆 100 GiB Persistent Disk。`lsblk -f` 目前沒有顯示它的檔案系統或掛載點；先確認是否有資料與原用途，才決定保留、使用或清理。**不要在未確認前格式化或刪除。** 停止 VM 可省運算／GPU 使用費，但保留的 Persistent Disk 等資源仍可能收費。[GCP 停止 VM](https://docs.cloud.google.com/compute/docs/instances/stop-start-instance)
