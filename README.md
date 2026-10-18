# HPC AI 效能工程師：單 GPU 作品路線

這份規劃直接對應職缺的四項工作：**測試自動化與數據分析、機器學習效能分析、LLM 訓練效能分析、分散式系統軟硬體調校**。唯一硬體限制是最多一張 GPU。作品主角是效能工程方法與可重現的診斷；本機或雲端 Linux 單卡皆可完成核心作品。已有叢集可以用作實驗環境，但不決定作品題目。

依[模組學習路線](curriculum/ROADMAP.md)、[技術觀念講義](curriculum/CONCEPTS.md)與[作品成果對照](curriculum/OUTCOMES.md)進行，實際結果記在[學習進度](PROGRESS.md)：每個模組學觀念、寫程式、做實驗、分析結果，再把實際成果接到下一個模組。**不設定週數或每日進度。**下方是最終作品設計，各模組文件是實作入口。

## 最終成果

交付一個 **AI Performance Lab** 倉庫，保存基準數據、profiler trace、瓶頸假設、調校決策、調校前後的效能與代價、重現命令，以及無效或不確定的結果。主作品是 LLM **訓練**效能；推論服務列為選修延伸。

| 職缺能力 | 必做證據 | 優先級 |
|---|---|---|
| 測試自動化與數據分析 | 可重跑的實驗 CLI、環境快照、原始數據、統計與回歸判定 | 最高 |
| ML 效能分析 | 真實資料載入、前反向、CPU/GPU timeline、瓶頸調校案例 | 高 |
| LLM 訓練效能分析 | decoder-only 訓練與開源模型微調、tokens/s、顯存、profile、受控 A/B | 最高 |
| 分散式系統調校 | CPU 多節點 collective、網路與儲存路徑、單卡資料供給、擴展模型與限制 | 高 |
| Linux、C/C++、Python、系統架構 | Python 量測平台、C++/CUDA 微基準、CPU/PCIe/記憶體／網路分析 | 高 |

## 加分條件如何變成證據

加分項要嵌在主作品中，不能只在 README 列技術名詞。下表是**完成門檻**；同一份實驗可以同時證明多項能力。標示「條件式」的實測需有相應硬體，不用日曆時間或任意優先級跳過能力。

| 加分條件 | 具體證據 | 所屬模組 |
|---|---|---|
| Linux 系統效能分析 | 在 ML/LLM 報告中附 `perf stat`／`pidstat`／`iostat` 等可用指標，定位 CPU、I/O 或排程等待；結合 GPU trace 解釋端到端瓶頸。受權限限制的計數器需標示不可用。[Linux workload tracing](https://docs.kernel.org/admin-guide/workload-tracing.html) | 01、04–06 |
| GPU、ML frameworks、LLM | PyTorch 訓練 loop、Profiler、CUDA/Nsight trace、真實模型微調和三輪受控調校；交付的不是框架教學，而是效能判斷 | 03–06 |
| 分散式系統、網路協定 | Gloo/MPI 訊息大小掃描；用 `ss -ti`、NIC 統計與封包擷取核對 TCP RTT、retransmit、吞吐、MTU 和 CPU 開銷，解釋 collective 與資料供給的曲線 | 07–08 |
| RDMA | 先做一份 **TCP 與 RDMA 資料路徑設計／診斷報告**：記憶體註冊、queue pair、completion、RoCE/InfiniBand 的前提、PFC/ECN/CNP 與錯誤計數器；寫出若有 RDMA NIC 時會如何用 `ibv_devinfo`、`rping`／perftest 和 NIC counters 驗證。只有取得相容硬體時才新增實測，明確區分設計與量測。[NCCL 網路疑難排解](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html) | 10；實測條件式 |
| 雲端運算 | 用一份可重現的 VM／容器環境規格或 IaC 部署單 GPU 實驗，記錄機型、映像、磁碟、驅動、網路、開關機流程、每次 GPU 小時及成本；換新機後能重跑基準。若使用本地 GPU，也要提供雲端部署設計與成本估算，標成未部署 | 11 |
| 資料庫 | `perfctl` 以 SQLite 建立 run／environment／metric 索引；JSONL 保留原始數據。以實際查詢比較索引前後的 `EXPLAIN QUERY PLAN` 和查詢時間，記錄 WAL 與備份策略。SQLite WAL 不適合跨主機共享資料庫，跨節點寫入由單一收集器集中處理。[SQLite query plan](https://www.sqlite.org/eqp.html)、[SQLite WAL](https://www.sqlite.org/wal.html) | 02 |
| 伺服器或儲存系統 | 比較本機磁碟、遠端資料及 checkpoint 寫入對訓練 stall 的影響；記錄 `iostat`、實際讀寫量、page cache、檔案系統、磁碟型號與容量。若有遠端儲存，測一致的資料集與冷／熱 cache 條件 | 09 |
| 開源社群貢獻 | 在用到的上游專案提出一個可重現 issue、文件修正、benchmark bug fix 或小型 PR，附最小重現、版本與前後證據；倉庫連結 issue/PR 與審查狀態。**提交**可自行完成，合併與否取決於維護者，不能預先宣稱 | 12 |

上述 RDMA 設計報告要分析 TCP 與 RDMA 資料路徑差異，寫明哪些 TCP 量測結果不能外推到 RDMA。雲端、資料庫與儲存也要回到訓練的啟動、量測、資料供給或 checkpoint 問題，避免形成無關的小專案。

## 作品 1：效能實驗與回歸平台（模組 01–02）

建立 `perfctl` Python CLI。由 YAML 規格產生實驗矩陣；執行前檢查 CPU/GPU、顯存、驅動、CUDA、套件版本、磁碟與資料；暖機後重複執行；保存完整命令、git commit、環境快照、stdout/stderr、退出碼、每筆 step 時間和 GPU 記憶體。輸出 JSONL 原始資料、CSV 摘要、Markdown 報告及可重生的圖。失敗、OOM、逾時和環境不一致必須可見。

比較器只對**同一工作負載、同一精度、同一有效 batch、同一硬體**作 A/B；顯示中位數、分散程度、相對差異、樣本數與原始分布。至少五次獨立重複。P95 延遲另用每組至少 100 個成功 step／請求作起始樣本數，並揭露失敗率；五次重複本身不足以估 P95。GPU kernel 用 CUDA event 或同步處理非同步執行，訓練 step 端到端時間用主機時鐘，兩種時間分開報。[PyTorch CUDA 計時](https://docs.pytorch.org/docs/stable/notes/cuda.html)、[PyTorch benchmark 工具](https://docs.pytorch.org/docs/stable/benchmark_utils.html)

**作品結果**：同一個矩陣乘法／小模型，在不同 batch 下自動完成基準；故意加入 OOM 或錯誤參數，證明失敗不會被算成性能改善；從保存的 JSONL 可以獨立重算圖表。

## 作品 2：ML 訓練管線瓶頸定位（模組 04）

選一個規模可控的影像分類模型和授權清楚、版本固定的公開資料集。資料先下載並固定在本機；提供合成資料對照，以區分「模型計算能力」和「資料供給能力」。完整跑資料讀取、解碼／變換、H2D、前向、反向、optimizer；記錄 samples/s、每 step 時間、峰值顯存、CPU 忙碌、資料等待和 GPU 空檔。用 PyTorch Profiler 標註區段並匯出 trace；必要時用 Nsight Systems 核對 CPU 與 CUDA timeline。[PyTorch Profiler](https://docs.pytorch.org/tutorials/recipes/recipes/profiler_recipe.html)、[Nsight Systems](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)

做**兩個診斷循環**，只針對 trace 顯示的瓶頸調整，例如資料 worker/prefetch/pinned memory、batch size、H2D 傳輸，或算子／資料布局。每次先寫預期哪段時間會縮短，再實測；同時記錄 CPU、RAM、顯存與模型正確性／loss。若資料載入原本不是瓶頸，就不為了湊成果去調 worker。[PyTorch 資料載入最佳化](https://docs.pytorch.org/tutorials/intermediate/intermediate_data_loading_tutorial.html)

**作品結果**：一份 timeline、一張 step 時間分解圖、兩輪 A/B 原始數據，以及「為何採用或放棄此調整」的工程判斷。這份作品呈現一般 ML 系統的分析過程。

## 作品 3：單 GPU LLM 訓練效能分析（模組 05–06，主作品）

### 兩層工作負載

1. **可控的 decoder-only 小模型**：用 PyTorch 跑真正的前向、反向和 optimizer step。層數、hidden size、序列長度、microbatch 可設定；固定 token 資料和種子。用它隔離 attention、MLP、optimizer 和資料路徑，建立可解釋的基準。
2. **真實開源模型微調**：選單卡可容納且授權清楚的小型預訓練 causal LM，固定 checkpoint、tokenizer、資料集版本。做 full fine-tuning（若可容納）或 LoRA，並清楚區分兩者；LoRA 降低可訓練參數與 optimizer 狀態，**不能代表全參數訓練效能**。[Hugging Face PEFT 說明](https://huggingface.co/docs/peft/main/package_reference/lora)

### 必量指標

以 **non-padding training tokens/s** 作主要吞吐指標，另報 step latency、每秒有效 optimizer 更新數、GPU 峰值已分配／保留顯存、資料等待時間、前向／反向／optimizer 時間、loss 或梯度異常。記錄 microbatch × gradient accumulation 的有效 batch、序列長度分布、精度和 tokenizer。若比較不同有效 batch，分開報告，不把它寫成純粹的性能改善。

### 受控實驗矩陣

| 問題 | 變因 | 要回答的工程問題 |
|---|---|---|
| GPU 是否吃飽？ | microbatch、序列長度、padding 比例 | 是小批次／padding 浪費，還是已接近顯存與計算限制？ |
| 記憶體與速度如何交換？ | bf16/fp16（依硬體支援）、activation checkpoint | 顯存省了多少，額外計算耗時多少，能否換來更大 microbatch？ |
| attention 是否為主要瓶頸？ | PyTorch SDPA 支援的 backend | 實際使用哪個 backend？改變後 attention、整步和顯存各有何變化？ |
| optimizer 或資料供給是否主導？ | optimizer 選項、預先 tokenized 資料／即時處理 | bottleneck 轉移到哪裡？整體訓練收益是否存在？ |

一次只改一個主要變因；只有 profiler 證據支持時才做下一輪。硬體或版本不支援的精度與 kernel 就排除並記錄。Activation checkpointing 用計算換記憶體；SDPA 的收益依硬體和輸入而異，需量測實際 backend。[PyTorch checkpointing](https://docs.pytorch.org/docs/stable/checkpoint)、[PyTorch SDPA](https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html)、[Transformers 單 GPU 訓練指南](https://huggingface.co/docs/transformers/main/perf_train_gpu_one)

**作品結果**：至少三個有完整假設、trace、A/B 與結論的實驗；其中一個聚焦瓶頸改善，一個聚焦速度／顯存取捨，一個展示無效或反效果調整。主報告回答「這張卡在這個工作負載的最佳已測設定是什麼、適用範圍到哪裡」。

## 作品 4：單卡條件下的分散式系統效能（模組 07–10）

把「可真正測到」和「可推估但未驗證」分開：

- **真實多節點通訊**：兩台普通 Linux CPU 主機即可用 PyTorch Gloo 或 MPI 做 `all_reduce`、broadcast 的大小掃描，量測啟動成本、延遲、有效頻寬、CPU 使用率和網路流量。只有一台主機時先做多 process 功能版，再等第二台補多節點數據。PyTorch 建議 CPU 分散式工作使用 Gloo。[PyTorch 分散式文件](https://docs.pytorch.org/docs/stable/distributed.html)
- **單 GPU 的遠端資料路徑**：固定同一訓練工作，對照本機資料、遠端檔案／物件儲存或網路串流；觀察資料等待、GPU idle、吞吐、page cache 與網路使用。只有確有遠端來源時才做；不能用本機迴圈連線冒充跨節點網路。
- **擴展模型**：以實測的單卡 compute 時間、CPU collective 延遲和資料路徑數據，建立簡單的 compute/communication 時間模型，列出假設與敏感度。它是設計練習，**不是**多 GPU scaling 結果。

若環境有 Slurm，加入作業放置、CPU affinity、資源配額與共享檔案系統的比較；沒有 Slurm，核心實驗仍可完成。RDMA、NCCL、多 GPU DDP、NVLink 或 GPU Direct 必須有相應硬體才能宣稱實測。尤其不能讓兩個 NCCL rank 共用一張 GPU 假裝做雙卡 benchmark；PyTorch 文件要求多 process 使用 NCCL 時每個 process 獨占其 GPU。[PyTorch 分散式文件](https://docs.pytorch.org/docs/stable/distributed.html)

**作品結果**：訊息大小對延遲／有效頻寬曲線、訓練資料位置對 GPU 等待和 tokens/s 的比較（若有遠端來源）、一份標明已測／推估／未測的調校建議。

## 作品 5：系統與 C++／CUDA 深度證據（模組 03）

寫一個有 CPU 參考答案的 C++／CUDA microbenchmark，量測 H2D、kernel、D2H 和端到端時間；至少比較兩種資料布局或 block size。分析有效頻寬與輸入大小的關係，用 Nsight Compute 或可用的 kernel 指標檢驗瓶頸假設。另測 host CPU 記憶體頻寬或 NUMA／affinity（硬體若有多 NUMA domain）；把系統拓撲、PCIe、資料移動代價連回 LLM 訓練 trace。性能改善須先通過數值正確性。[CUDA Best Practices](https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/index.html)、[Nsight Compute](https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html)

這個作品是底層能力證據；它服務於主作品中的具體瓶頸，不另做與 AI 工作負載無關的大型 CUDA 專案。

## 倉庫成品與交付門檻

```text
ai-performance/
  README.md                  # 職缺對照與成果入口
  pyproject.toml             # perfctl 套件與固定依賴
  configs/                   # 實驗矩陣、模型與資料版本
  src/ai_perf/               # 預檢、量測、統計、比較、報告
  infra/                     # VM／容器環境與成本記錄
  workloads/ml/              # ML 完整訓練管線
  workloads/llm/             # decoder-only 與真實模型微調
  workloads/distributed/     # Gloo/MPI 與資料路徑
  workloads/cuda/            # C++/CUDA 微基準
  results/                   # 可公開的小型原始資料與圖表
  reports/                   # 每個瓶頸案例與總結
  contributions/             # 上游 issue／PR、最小重現與審查狀態
```

每份報告固定六段：**問題與假設、環境與工作負載、量測方法、原始數據和圖、診斷與變更、限制與下一步**。要有簡短的英文 executive summary，因職缺要求英文閱讀與溝通。大型 trace、模型權重與資料不進 git，提供取得方式和校驗資訊。

完成一個模組的驗證與證據後進下一模組；任何模組若缺硬體或權限，先完成可實測部分，將未驗證項目標明並保留補測入口。推論服務、vLLM TTFT/TPOT、Grafana 儀表板和更複雜的 Slurm 自動化列為延伸，因本職缺明確強調 LLM **訓練**效能。

現有叢集作品可以提供 GPU 與 CPU 節點、Slurm 排程或故障案例，但它是實驗場地，不能替代上述效能作品。所有性能數字都等實測後再寫；現階段不預填提升百分比。
