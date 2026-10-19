# 官方參考與工具選擇

文件入口整理日期：2026-10-19。官方 stable/main 頁會更新；實作時記錄安裝版本並讀相符版本文件。這些來源支援技術學習，不代表已查證雇主內部工具清單。

| 週 | 工具／觀念與用途 | 官方來源 |
|---|---|---|
| 1、5–6 | sysstat 系統採樣、perf CPU 分析 | [sysstat](https://sysstat.github.io/)、[Linux perf](https://perfwiki.github.io/main/) |
| 2–3 | Python 語法、subprocess、計時、資料紀錄 | [Python tutorial](https://docs.python.org/3/tutorial/)、[標準函式庫](https://docs.python.org/3/library/) |
| 4–6 | GCC、sanitizer、自動向量化、OpenMP | [GCC 文件](https://gcc.gnu.org/onlinedocs/)、[OpenMP](https://www.openmp.org/specifications/) |
| 7–8 | CUDA 執行模型、記憶體與同步 | [CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-programming-guide/)、[Compute Sanitizer](https://docs.nvidia.com/compute-sanitizer/ComputeSanitizer/index.html) |
| 9、12、16 | CPU/GPU 時序與 kernel 計數器 | [Nsight Systems](https://docs.nvidia.com/nsight-systems/UserGuide/)、[Nsight Compute](https://docs.nvidia.com/nsight-compute/ProfilingGuide/) |
| 10 | NumPy 陣列與形狀 | [NumPy basics](https://numpy.org/doc/stable/user/basics.html) |
| 11–13 | tensor、autograd、Dataset、ML 訓練與 profiler | [PyTorch basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)、[Profiler](https://docs.pytorch.org/docs/stable/profiler.html)、[AMP](https://docs.pytorch.org/docs/stable/amp.html) |
| 14–17 | Attention/Transformer 與標準模型 | [原始 Transformer 論文](https://arxiv.org/abs/1706.03762)、[SDPA](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)、[checkpoint](https://docs.pytorch.org/docs/stable/checkpoint.html)、[GPT-2](https://huggingface.co/docs/transformers/model_doc/gpt2) |
| 18 | TCP 吞吐、反向與 JSON 報表 | [iperf3](https://software.es.net/iperf/invoking.html) |
| 19 | 跨主機啟動與 MPI API | [Open MPI launching](https://docs.open-mpi.org/en/main/launching-apps/quickstart.html)、[MPI Forum](https://www.mpi-forum.org/docs/) |
| 20 | 控制器、節點、作業與 MPI 整合 | [Slurm admin](https://slurm.schedmd.com/quickstart_admin.html)、[srun](https://slurm.schedmd.com/srun.html)、[MPI guide](https://slurm.schedmd.com/mpi_guide.html) |
| 21 | Gloo、DDP、torchrun、sampler | [PyTorch distributed](https://docs.pytorch.org/docs/stable/distributed.html)、[DDP tutorial](https://docs.pytorch.org/tutorials/intermediate/ddp_tutorial.html) |
| 22 | I/O 工作量與 fio 指標 | [fio 文件](https://fio.readthedocs.io/en/latest/fio_doc.html) |
| 23 | verbs、perftest、NCCL 路徑與性能口徑 | [rdma-core](https://github.com/linux-rdma/rdma-core)、[perftest](https://github.com/linux-rdma/perftest)、[NCCL troubleshooting](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)、[nccl-tests performance](https://github.com/NVIDIA/nccl-tests/blob/master/doc/PERFORMANCE.md) |

Google Cloud 硬體選修：[Cloud RDMA 建立條件](https://docs.cloud.google.com/compute/docs/instances/create-vm-with-rdma)。可用性、價格、配額使用前再查，不把網頁支援當專案已具備。
