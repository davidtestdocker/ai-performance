# 技術觀念講義

本講義補足各模組的概念起點。重點是在作品實驗裡觀察這些現象、理解原因與限制。工具版本或硬體支援項目以實際環境核對。

## 01 量測與系統瓶頸

- **延遲與吞吐**：延遲是單件工作的完成時間，吞吐是單位時間完成量。提高 batch 可能增加吞吐，同時拉高單件延遲；必須先說明目標是哪一個。
- **CPU time 與 wall time**：CPU time 累計程序使用 CPU 的時間；wall time 包含等待 I/O、排程和 GPU。多執行緒 CPU time 甚至可大於 wall time。兩者差距是線索，不能單獨判定瓶頸。
- **利用率與飽和**：某段時間 GPU 忙碌比例高，不代表實際 tokens/s 已達此工作負載最佳值；小 kernel、記憶體等待和排隊都可能造成高利用率。需結合吞吐、trace、顯存與硬體指標。
- **非同步與暖機**：CPU 發出 CUDA 工作後，通常不用等 GPU 做完就會繼續往下走。所以只量「發出指令花多久」，會把 GPU 執行時間算得太短。若要量某個 GPU kernel（在 GPU 上執行的函式）本身，可在它前後放 CUDA event，讀取 GPU 端經過的時間；若要量整段程式實際等了多久，可用主機時鐘計時，但在停止計時前必須等 GPU 完成（同步）。後者也會包含 CPU 發出工作等額外時間，不能直接當成純 kernel 時間。第一次執行還可能包含初始化或編譯；先跑幾次讓它進入穩定狀態（暖機），再正式量測。[PyTorch CUDA 說明](https://docs.pytorch.org/docs/stable/notes/cuda.html)
- **可比較性**：比較「修改前後誰比較快」時，先讓硬體、軟體版本、輸入資料、工作量、數值精度與有效 batch（每次更新模型參數所用的樣本數）相同，再重複量測，看看結果會波動多少。P95 是「95% 的單次耗時不超過這個值」：例如記錄 100 次請求，將耗時由小到大排列，約第 95 個值就是 P95；它用來看較慢的那一端，樣本太少時容易失真。若修改前後的耗時波動範圍大量重疊，先不要說效能已改善。


## 02 自動化、統計與資料庫

- **實驗的最小單位**：一次 run 要有輸入、版本、資源、命令、開始／結束、退出碼與原始量測；run 結束後不能悄悄修改原始資料。摘要由原始資料生成。
- **獨立重複與逐筆樣本**：不同 run 可觀察環境波動；同一 run 的 step 延遲可看尾端分布。這兩種樣本不能混為一談。失敗 run 既不能當成功數字，也不能被藏起來。
- **回歸判定**：比較相同條件下的差異及波動；報告變因、樣本數、效應量和不確定性。不要只靠單次最快值。多個實驗同時跑在同一張 GPU 會相互干擾。
- **JSONL 與 SQLite**：JSONL 保存逐筆事件，SQLite 方便按環境、模型、版本查詢。index 可加速查詢但增加寫入與空間成本；用 `EXPLAIN QUERY PLAN` 核對，不靠猜測。[SQLite 查詢計畫](https://www.sqlite.org/eqp.html)
- **WAL 邊界**：SQLite WAL 容許本機讀寫並行，但不能把 WAL DB 放在跨主機共享檔案系統當集中服務；多節點原始結果交由單一收集器匯入。[SQLite WAL](https://www.sqlite.org/wal.html)


## 03 GPU、C++ 與 CUDA

- **執行階層**：grid 由 block 組成，block 的 thread 以 warp 方式執行。block size 改變佔用、排程與記憶體存取；較大不一定較快。
- **記憶體路徑**：host→device、device kernel、device→host 各有成本。只看 kernel 時間會漏掉傳輸；對小工作負載，啟動與傳輸可能主導端到端時間。
- **有效頻寬**：估算 `bytes_read + bytes_written`，除以 kernel 秒數得到 GB/s；估算必須說明讀寫次數、快取命中與單位。它是對工作負載有用的吞吐，不等於記憶體晶片的理論峰值。[CUDA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)
- **算術強度**：每讀寫一 byte 做多少運算，幫助判斷算力與頻寬哪個較可能限制；需搭配實際指標，不以單一公式取代 profiling。
- **正確性優先**：不同資料布局、block size、精度若改變數值答案，必須按誤差容忍度檢查；不正確的快速結果不算優化。


## 04 ML 訓練管線

- **完整 step**：資料讀取／解碼／變換、batch 合併、H2D、前向、loss、反向、optimizer。任何一段都可讓 GPU 空轉，Profiler 區段要能對應這條路徑。
- **合成與真實資料**：合成資料把 I/O／解碼因素拿掉，可測上界，但不能代表部署後吞吐。真實資料的長尾讀取時間可能更關鍵。
- **DataLoader 取捨**：增加 worker 可減少主線等待，也會增加 CPU/RAM、process 啟動與資料複製成本。pinned memory 與非阻塞傳輸只有配合實際資料路徑才可能受益。[PyTorch 資料載入教學](https://docs.pytorch.org/tutorials/intermediate/intermediate_data_loading_tutorial.html)
- **Profiler 開銷**：trace 收集會改變執行時間。性能結論用低開銷的重複量測；trace 用來定位，不直接把帶 profiler 的時間當常態吞吐。


## 05 LLM 訓練基準

- **decoder-only 訓練**：每個 step 有 tokenized input、causal attention、loss、反向、optimizer；必須證明參數更新且 loss/梯度有效，否則 tokens/s 可能只是推論速度。
- **有效 batch**：`microbatch × gradient_accumulation × data_parallel_world_size`。單 GPU 時最後一項是 1。不同有效 batch 會改變更新頻率與可能的學習行為，不能直接當純性能 A/B。
- **tokens/s 定義**：此課以實際參與 loss 的 non-padding training tokens 除以端到端訓練時間；若把 padding 或 warmup 算進去，結果會誤導。另報每秒 optimizer update 及序列長度分布。
- **顯存構成**：權重、梯度、optimizer state、activation 與框架保留空間。峰值已分配和保留顯存不同；不同微調法改變的部分也不同。
- **LoRA 邊界**：LoRA 只訓練低秩 adapter，降低可訓練參數與 optimizer 負擔；它的吞吐與顯存數據不能代表全參數微調。[PEFT LoRA](https://huggingface.co/docs/peft/main/package_reference/lora)


## 06 LLM 調校與診斷

- **A/B 原則**：只改主要變因，固定模型、資料、精度、有效 batch 和環境；若調整 microbatch 連帶改了 accumulation，需明確保持或標示有效 batch 變化。
- **混合精度**：bf16/fp16 影響計算與顯存，也可能改變數值穩定性；先確認硬體、kernel 與框架支援，再檢查 loss/梯度。
- **activation checkpointing**：不保存部分 activation，反向時重算，用更多計算換較少顯存。是否值得，要看能否換來較大 batch 或避免 OOM，並比較整步時間。[PyTorch checkpointing](https://docs.pytorch.org/docs/stable/checkpoint)
- **attention backend**：設定 SDPA 不代表一定選到期望的 kernel；shape、dtype、mask、硬體版本可能影響實際路徑。要核對 profiler trace、整步時間和顯存。[PyTorch SDPA](https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html)
- **瓶頸轉移**：改善 attention 後，資料載入或 optimizer 可能成為主瓶頸。每輪重新量測完整 step，保留無效調整的證據。


## 07 TCP 網路

- **RTT 與頻寬**：小訊息通常較受固定往返與啟動成本影響，大訊息較看有效傳輸速率；同一個「網路慢」需要用不同量測拆開。
- **重傳與壅塞**：TCP 會處理丟包和重傳；`ss -ti` 與 NIC/封包計數器可以提供線索，須對齊量測時間。重傳增加不必然代表應用瓶頸，還要看端到端效果。
- **MTU 與虛擬化**：MTU 不一致、封包分段、共享雲端網路與主機 CPU 都可能影響結果。單機 loopback 不經過實際 NIC，不能當跨節點基準。


## 08 分散式訓練機制

- **rank 與同步**：rank 是程序身分；`all_reduce` 合併所有 rank 的數值並把結果分發。每個 rank 需要驗證相同最終值，還要看它們是否真的在不同主機上。[PyTorch 分散式文件](https://docs.pytorch.org/docs/stable/distributed.html)
- **DDP 與 FSDP**：DDP 在各 rank 保存模型副本並同步梯度；FSDP 切分參數、梯度和 optimizer state，在前向／反向期間 all-gather 所需參數，反向後 reduce-scatter 梯度。比較兩者要看每卡記憶體、通訊量、同步點及能否與計算重疊。[PyTorch DDP](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html)、[PyTorch FSDP2](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html)
- **其他模型並行**：張量並行切分單層計算，流水線並行把層分到不同裝置；選擇取決於模型能否放進單卡、裝置間連線和負載形狀。單 GPU 學資料切分與通訊時機，不能實測兩者擴展率。[PyTorch 張量並行](https://docs.pytorch.org/tutorials/intermediate/TP_tutorial.html)、[PyTorch 流水線並行](https://docs.pytorch.org/tutorials/intermediate/pipelining_tutorial.html)
- **CPU Gloo 與 GPU NCCL**：少量 CPU Gloo 實作能學 process group、rank、rendezvous 和 collective 正確性；它的延遲與頻寬不能代入 NCCL。PCIe／NVLink、跨節點網路、RDMA 與 GPU 拓撲會改變通訊路徑。只有實際多 GPU 才能量測擴展率。[NCCL 總覽](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/overview.html)
- **工作配置與訓練執行**：Slurm 分配節點、CPU 和 GPU，`torchrun` 啟動 PyTorch process；兩者可一起使用。分析 Slurm 工作時要分開佇列等待、啟動和穩態 step。GPU GRES 與 CPU binding 可能改變工作實際看到的資源，但仍需量測才能說有性能影響。[Slurm GRES](https://slurm.schedmd.com/gres.html)、[CPU 管理](https://slurm.schedmd.com/cpu_management.html)


## 09 伺服器與儲存

- **page cache**：重複讀取可能從 RAM 命中而非磁碟；冷／熱 cache 結果都要標示條件。不要用不受控的系統 cache 清除干擾其他工作。
- **checkpoint 成本**：序列化、CPU/GPU 資料轉移、寫入、`fsync` 與遠端同步都可能停頓訓練；checkpoint 頻率是恢復點與吞吐的取捨。
- **儲存層次**：本機 SSD、共享檔案系統、物件儲存有不同 API、延遲和一致性方式；不能只以一個 MB/s 比較訓練效果。


## 10 RDMA

- **資料路徑**：RDMA 讓具備能力的 NIC 在已註冊記憶體上執行傳輸；概念上可減少 CPU 參與和複製，但實際收益依硬體、工作負載、網路設計與軟體而定。
- **操作物件**：queue pair 提供傳輸端點，work request 提交工作，completion queue 回報完成；理解記憶體註冊及錯誤／重試行為，才能解讀診斷工具。
- **RoCE 前提**：RoCE 的壅塞與無損網路設定需要檢查 NIC/交換器計數器，例如 PFC、ECN/CNP、丟包及錯誤；只看到連線成功不代表效能健康。[NCCL 網路疑難排解](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html)
- **證據邊界**：沒有相容 RDMA NIC 與兩端路徑，就只能交付設計和 runbook；TCP 或單 GPU 測量不能改名為 RDMA／GPU Direct 結果。


## 11 雲端重現

- **環境分層**：VM image、host GPU driver、容器 runtime、CUDA runtime、PyTorch wheel、模型與資料版本都會影響可用性和數字。容器固定依賴，不能代替 host driver。
- **成本與可比性**：記錄機型、GPU、磁碟、網路、啟停時間及 GPU 小時；不同機型的數字不能直接當軟體回歸。空閒 VM 也可能繼續產生成本。
- **重建測試**：從乾淨機器依文件部署、執行短基準、比較環境快照；失敗修復必須回寫部署文件。


## 12 開源與作品記錄

- **最小重現**：issue 要有版本、輸入、命令、預期／實際結果與最小案例；維護者不應需要整個叢集才能理解問題。
- **貢獻狀態**：提出、審查中、合併、關閉是不同狀態；履歷只寫已發生的事。文件修正也要有清楚的問題和驗證。
- **證據鏈**：履歷敘述連回程式、命令、原始資料、圖和判讀。大型結果可另存，但要提供版本與校驗資訊。
