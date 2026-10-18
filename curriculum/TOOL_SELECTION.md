# 這份職缺的工具選型與學習順序

[模組路線](ROADMAP.md)｜依使用者提供的職缺內容判斷。職缺直接要求測試自動化、ML 與 LLM **訓練**效能分析、分散式系統調校，以及 Linux、C/C++、Python；加分項包括 GPU、網路、RDMA、雲端、資料庫、伺服器／儲存和開源。**職缺沒有指定 Slurm、Ray、Kubernetes 或某個 LLM 框架。**工具選型因此以能否產生可重現的效能證據為先，不以品牌數量為目標。

## 判斷準則

1. 它是否直接幫助量測、定位或修正職缺中的問題？
2. 它是否是所學概念的代表性實作，技能能否轉移到另一套平台？
3. 在最多一張 GPU 下能實測什麼？無法實測的部分要清楚分開。
4. 引入它會不會把時間從 LLM 訓練效能主線移走？

## 主線工具

| 能力層 | 選用工具 | 在作品中做什麼 | 單 GPU 能證明什麼 |
|---|---|---|---|
| 可信基準與自動化 | Python、JSONL/SQLite、PyTorch benchmark／CUDA Event；參照 MLPerf Training 的模型、品質與系統資訊揭露方法 | 固定工作負載、品質條件、版本與統計口徑；比對整體訓練時間、step、吞吐和錯誤 | 自製基準可重現。不能稱為正式 MLPerf 成績；MLPerf Training 衡量訓練到目標品質的時間，正式提交有規則。[MLCommons Training](https://mlcommons.org/benchmarks/training/) |
| Linux／伺服器觀察 | `pidstat`、`iostat`、`perf`、`ss`、`ethtool`；可用時加 NVIDIA DCGM | 分辨 CPU、I/O、網路、GPU 忙碌、時脈／功率／溫度異常 | 單機系統瓶頸和 GPU 健康狀態。DCGM 的支援欄位依設備而異。[NVIDIA DCGM](https://docs.nvidia.com/datacenter/dcgm/latest/learn/modules/profiling.html) |
| GPU 程式與 profiler | C++/CUDA、PyTorch Profiler、Nsight Systems、Nsight Compute | 先定位端到端空檔，再下鑽 kernel／記憶體問題；數值正確性與速度一起看 | 單卡 kernel、H2D/D2H、GPU/CPU timeline。[PyTorch Profiler](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)、[CUDA 最佳實務](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html) |
| ML／LLM 訓練 | PyTorch、Transformers、PEFT；先有可控訓練 loop，再跑真實開源模型 | 資料供給、前反向、optimizer、precision、SDPA、checkpoint、必要時 `torch.compile`；同時量測速度、顯存與 loss／品質 | 單卡訓練與微調的性能取捨。[PyTorch 調校指南](https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide)、[Transformers 單卡訓練](https://huggingface.co/docs/transformers/main/perf_train_gpu_one) |
| 分散式計算基礎 | `torchrun`、`torch.distributed`／Gloo；學 DDP／FSDP／NCCL 機制，沿用既有 MPI 經驗 | 小型 CPU Gloo 實作驗證 rank 與 collective 正確性；畫出多 GPU DDP／FSDP 的資料移動、顯存取捨和待測通訊點 | CPU 程序語意可驗證；多 GPU 通訊效能與擴展率仍未測。[PyTorch distributed](https://docs.pytorch.org/docs/stable/distributed.html)、[FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html) |
| HPC 作業執行 | **Slurm 作具體平台**：`sbatch`、`srun`、GPU GRES、CPU binding、工作記錄 | 對同一訓練工作記錄資源配置、節點放置、CPU 可用集合與執行時間；佇列等待與工作內效能分開 | 單 GPU Slurm 配置對訓練效能的影響；不需要再建一套叢集。[Slurm GRES](https://slurm.schedmd.com/gres.html)、[CPU 管理](https://slurm.schedmd.com/cpu_management.html) |

**實驗順序**：先讓一個真實訓練工作正確且可重跑 → 用 PyTorch Profiler/Nsight 和 Linux/GPU 指標定位 → 做控制變因的調校 → 將同一工作放進 Slurm 資源配置下比較 → 用 CPU Gloo 驗證多程序語意，並將 DDP／FSDP／NCCL 的待測點對應到單卡 trace。真實網路性能由模組 07 量測。每一步都沿用同一組環境記錄和原始資料。MLPerf 的品質／揭露原則可借用；不做符合規則的正式提交就不使用 MLPerf 名稱宣稱成績。

## 依工作情境選用的工具

| 工具或框架 | 何時值得學到實作 | 此作品的決定 |
|---|---|---|
| Ray Core／Ray Train | 工作需要動態 Python task、actor、資料處理或團隊明確使用 Ray；Ray Train 管 worker 與資源，但不取代模型 profiler 或 GPU collective。[Ray 資源模型](https://docs.ray.io/en/latest/ray-core/scheduling/resources.html)、[Ray Train](https://docs.ray.io/en/latest/train/train.html) | 先理解角色，不列必做。若有真實 Ray 工作流，再增加同負載的啟動／穩態比較；Ray 也可在 Slurm 配置內運行。[Ray on Slurm](https://docs.ray.io/en/latest/cluster/vms/user-guides/community/slurm.html) |
| NCCL tests、DDP/FSDP 多 GPU 實測 | 取得至少兩張適用 GPU 或客戶環境時，用來量測 collective、拓撲與擴展 | 學語意與診斷；本機只有一張 GPU，不以單 rank 的 NCCL tests 冒充通訊性能。[NVIDIA NCCL tests](https://github.com/NVIDIA/nccl-tests) |
| RDMA／GPU Direct | 有相容 NIC、網路與 GPU 拓撲時，才能做性能與故障實測 | 先做資料路徑和診斷設計，明確標「未實測」。[NCCL 網路排錯](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html) |
| Kubernetes、DeepSpeed、Megatron-LM | 團隊的部署或大模型訓練棧使用時 | 了解它們解決的資源或模型切分問題；不在單 GPU 作品中同時安裝以湊工具清單 |
| vLLM、推論服務 | 工作範圍擴展到推論延遲、吞吐、服務容量時 | 延伸。此職缺原文把 LLM **訓練**列為核心 |

## 現有路線需要補的內容

- 模組 01 加入 GPU 時脈、功率、溫度與錯誤狀態的環境觀察；若有 DCGM 才收相應欄位。
- 模組 02 的比較報告要記錄訓練品質／loss 與完整系統資訊；借用 MLPerf 的公平比較觀念，不宣稱 MLPerf 成績。
- 模組 05–06 的速度改善必須維持模型、資料與品質條件；`torch.compile` 是 profiler 顯示 Python/launch overhead 時的候選調整。
- 模組 08 加入 Slurm 對同一工作負載的資源配置與作業內性能觀察，以及 `torchrun` 的角色；Ray 保持條件式延伸。
