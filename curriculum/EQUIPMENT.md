# 設備限制與環境準備

確認日期：2026-10-19。此文件是規劃，不是雲端資產盤點。本次未開關 VM、未安裝雲端套件、未量測任何硬體。

## 必修資源

| 用途 | 配置方向 | 限制與驗收 |
|---|---|---|
| Linux/Python/C/C++ | 一台可登入 Linux CPU VM | 少量資料先跑，記 OS、vCPU、RAM、磁碟、版本 |
| 單卡 CUDA/ML/LLM | 一台含一張 NVIDIA GPU 的 VM | 使用既有可用 GPU；記實際型號/顯存/driver/toolkit，模型從小尺寸開始 |
| TCP/MPI/Slurm/Gloo | 兩台不同 CPU VM，2–4 vCPU、4–8 GiB 可作小實驗起點 | 不是保證足夠；依記憶體調小資料/模型，同 zone 私網優先，不能以同機容器替代 |
| Slurm controller | 可共用其中一台 CPU VM | 揭露控制與計算競爭，不強制第三台，也不省略真實兩 worker 驗收 |

GPU quota 最多一張。不要求新 GPU 或大型預訓練模型；小 GPT 從 2 layers、hidden 128、短序列、microbatch 1 起測，尺寸只是起點，不是已驗證保證。標準模型用小 config 隨機初始化真實訓練，避免下載大權重。

## 使用前逐步盤點

記錄 VM instance ID、hostname、zone、私有 IP、CPU/RAM、可用磁碟、OS/kernel、套件版本；GPU 記 nvidia-smi 和 nvcc，兩者版本意義不同。不要從舊課綱的機器名稱推斷現況。

按週安裝所需工具，不一次部署全部：W01 sysstat/time；W02–03 Python；W04–06 編譯器/OpenMP/perf；W07–09 CUDA/Nsight；W10 NumPy；W11–17 相容 PyTorch/Transformers；W18 iperf3；W19 MPI；W20 Slurm/MUNGE；W22 fio。使用隔離 Python 環境，保留精確版本及安裝命令，選與 driver/OS 相容的版本。官方來源見 [REFERENCES](REFERENCES.md)。

第一次安裝、服務與網路修改先確認具體環境和已有授權。僅開測試所需的私網存取；不把 MUNGE key、SSH key、token 或憑證提交 Git。結束後依實際需求關閉計費資源；停止 VM 不等於磁碟等所有費用停止。

## 受限環境的驗收

- VM 沒有 PMU/perf 計數器：保留錯誤，使用軟體事件、時間和系統指標；另列硬體補測方案。
- 只有一個 NUMA node：可實測 affinity，跨 socket 部分做原理與設計，不造假遠端記憶體結果。
- Nsight Compute 計數器不可用：保留限制，以 events、Systems timeline、工作量模型完成可支持的診斷；不可自行放寬全機權限政策。
- 顯存不足：縮小模型、序列或 microbatch，再明確記錄有效 batch；不刪掉 backward 或 optimizer 偷換成 inference。
- 第二台 CPU VM 暫不可用：跨節點日標受阻，不得改成同機完成；可整理已有證據，但必要跨節點驗收仍待實際資源。

## RDMA 與多 GPU：必修設計，選修硬體

RDMA 不必有 GPU，GPUDirect RDMA 才涉及 GPU 記憶體。現有環境是否提供 RDMA **待查證**，不能由單 GPU quota 推斷。Cloud RDMA 的 H4D 等機型需專用介面、driver、網路/placement 與區域容量；不把大型 H4D 當個人日常必備設備。

W23 必修：MR/QP/CQ、InfiniBand/RoCE/TCP 差異、collectives、NCCL 拓樸與診斷、FSDP/ZeRO/TP/PP 取捨、具體補測矩陣。多 GPU NCCL scaling、InfiniBand/RDMA/GPUDirect 硬體效能實測均選修；Soft-RoCE 只可標為軟體教學。CPU Gloo 或 TCP 數據不能替代 NCCL/RDMA 數據。

官方部署條件：[Cloud RDMA](https://docs.cloud.google.com/compute/docs/instances/create-vm-with-rdma)、[H4D](https://docs.cloud.google.com/compute/docs/compute-optimized-machines)。使用前重新核對規格、區域、配額與費用，課程不預先授權付費開機。
