# 模組 08：分散式訓練機制與工作放置

[路線](ROADMAP.md)｜目標：用少量 CPU 實作掌握 PyTorch 多程序語意，理解 DDP／FSDP 的資料移動與效能瓶頸，並分析 Slurm 資源放置對單卡訓練的影響。

[觀念講義](CONCEPTS.md)第 08 節｜[作品成果](OUTCOMES.md)

## 學習大綱

rank／process group／collective → CPU Gloo 最小正確性與 DDP 實作 → DDP／FSDP 通訊與記憶體路徑 → 張量／流水線並行的適用情境 → NCCL 與 GPU 拓撲 → Slurm 工作放置 → 多 GPU 故障診斷與待驗證實驗設計。

## 先理解

`world_size`、global/local rank、rendezvous、broadcast、all-reduce、all-gather、reduce-scatter、同步點與通訊／運算重疊。DDP 在各 rank 保留模型副本並同步梯度；FSDP 切分參數、梯度與 optimizer state，以額外通訊換取每卡記憶體空間。也要理解張量並行是切分單層運算，流水線並行是把不同層放在不同裝置；本作品只分析其適用情境，不做單卡模擬。CPU Gloo 可教程序協調與 collective 正確性，但網路與執行路徑不同，不能把其延遲或頻寬代入 GPU NCCL 擴展率。[PyTorch DDP](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)、[PyTorch FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)、[PyTorch 張量並行](https://docs.pytorch.org/tutorials/intermediate/TP_tutorial.html)、[NCCL 總覽](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html)

## 實作

1. 用 `torchrun` 啟動兩個 CPU process，以 Gloo 建立 process group，完成 `all_reduce` 和 broadcast；再用極小模型跑數個 DDP 更新，比對相同全域 batch 的單程序梯度／參數，理解資料切分與梯度平均。記錄 rank、hostname、輸入及輸出。若有第二台 CPU 主機，再驗證一次跨節點 rendezvous 與啟動。已有 MPI 跨節點經驗可直接沿用，不重做完整 CPU collective 性能掃描。
2. 用模組 05 的模型寫一份資料移動圖：DDP 每 rank 的模型、梯度與 optimizer state 在哪裡，反向傳播何時觸發梯度同步；FSDP 的 all-gather、reduce-scatter 與暫時展開參數發生在哪些階段。列出參數量、精度和每卡記憶體的估算式，標明 activation、暫存與框架開銷不在簡式估算中。
3. 對照單卡 profiler trace，標出若加入第二張卡，哪些區段可能出現 collective、等待或通訊／運算重疊。整理 NCCL 的 GPU 間資料路徑、PCIe／NVLink、跨節點網路與 RDMA 各自會影響哪些觀察值；寫出未來對「啟動卡住、某 rank 較慢、同步等待過長、顯存不足」分別要核對的 rank／節點記錄、GPU 拓撲、NCCL 日誌、collective 測試與訓練 profiler 指標。這一步只做機制與實驗設計，不產生多 GPU 效能數字。[NCCL 故障排查](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting.html)
4. 若有可用 Slurm 叢集，把同一單卡訓練工作以 `sbatch`／`srun` 提交，記錄 GPU GRES、`CUDA_VISIBLE_DEVICES`、CPU allocation／binding、節點、佇列等待、啟動與穩態 step 時間；只有在相同節點、GPU、資料和軟體條件下，才與直接執行及 `torchrun --nproc-per-node=1` 的**工作內**效能比較。Slurm 負責資源與工作啟動，`torchrun` 負責 PyTorch process 啟動；排隊時間不算進 GPU step 效能。[Slurm GRES](https://slurm.schedmd.com/gres.html)、[Slurm CPU 管理](https://slurm.schedmd.com/cpu_management.html)

## 做完留下的成果

Gloo rank／DDP 正確性程式與輸出、DDP／FSDP 資料移動和記憶體圖、張量／流水線並行適用情境、單卡 trace 上的多卡待驗證點，以及取得多 GPU 後可直接執行的量測與故障診斷設計。有 Slurm 時再附資源放置與穩態時間比較。所有圖表分清「單卡／CPU 已測」和「多 GPU 未測」。
