# 工具依問題逐步引入

[課綱](ROADMAP.md)

| 順序 | 工具 | 引入理由 |
|---|---|---|
| 00 | Python 時鐘、pidstat／vmstat、必要時 iostat、CUDA event | 先量對時間與系統活動，不一次教全部 Linux 工具 |
| 01 | PyTorch 最小 loop | 看懂張量、loss、梯度與參數更新 |
| 02 | Python subprocess、JSONL、簡單比較與繪圖 | 先自動化真實重複操作；有需要才加 CLI／YAML／SQLite |
| 03 | PyTorch Profiler，必要時 Nsight Systems | 先讀完整 CPU／GPU 路徑，再選調整 |
| 04 | C、C++、CUDA，必要時 Nsight Compute | 用正確性與資料移動解釋底層瓶頸 |
| 05–06 | PyTorch、Transformers；需要時 PEFT | 真實訓練、顯存與品質；AMP／SDPA／checkpoint／compile 各自按證據選用 |
| 07 | 既有 Slurm、TCP 工具、torchrun／Gloo | 資源配置、跨主機網路與程序語意；DDP／FSDP／NCCL 先理解資料路徑 |
| 08 | 固定容器與環境規格 | 用乾淨重跑驗證可重現性；host driver 仍須記錄 |

職缺未指定 Kubernetes、Slurm、Ray 或特定 LLM 框架。既有平台服務實驗，不把建平台當效能成果。SQLite 深度、Ray、vLLM、DeepSpeed／Megatron 與開源投稿是情境式延伸。

版本與硬體支援以實際環境核對；不強迫升到最新版。參考：[PyTorch tuning](https://docs.pytorch.org/tutorials/recipes/recipes/tuning_guide.html)、[CUDA semantics](https://docs.pytorch.org/docs/stable/notes/cuda.html)、[NCCL troubleshooting](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)。
