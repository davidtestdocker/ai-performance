# 固定課綱 v1.0：24 週 × 每週 5 日

核定日期：2026-10-19。唯一正式基準為本儲存庫 main 的本文件與各日 README。週次是學習順序，不是硬性日曆期限；未通過可延長練習，不得擅自移動、刪除或換掉週目標。

Python、C/C++、CUDA、PyTorch、ML、LLM 一律從零實作。只略過一般 Linux 操作入門，直接從系統效能與架構開始。閱讀舊聊天或舊程式不構成能力驗證。

| 週 | 固定目標 | 設備 | 必交成果 |
|---|---|---|---|
| [01 Linux 系統效能與 CPU 架構](weeks/week-01/README.md) | 建立 CPU、記憶體、程序與量測基線，能區分忙碌與等待。 | 一台 Linux CPU VM | 主機盤點、三種負載觀察表與基線報告 |
| [02 Python 從零與可重現紀錄](weeks/week-02/README.md) | 親手建立變數、流程、函式、檔案與錯誤處理能力。 | 一台 Linux CPU VM | 可讀寫 JSON/CSV 的小型實驗紀錄程式 |
| [03 自動化效能測試與數據分析](weeks/week-03/README.md) | 建立重複、錯誤分類、統計與可重現圖表的測試工具。 | 一台 Linux CPU VM | benchmark runner、原始 CSV、摘要圖與回歸規則 |
| [04 C 從零與記憶體正確性](weeks/week-04/README.md) | 從編譯、型別、指標開始親寫可驗證的 CPU kernel。 | 一台 Linux CPU VM；GCC/Clang | 具邊界測試與 sanitizer 紀錄的向量加法 |
| [05 C++ 從零與 CPU 記憶體效能](weeks/week-05/README.md) | 建立 C++ 資源管理並用工作集、SIMD 與 cache 解釋 CPU 效能。 | 一台 Linux CPU VM；perf 權限依環境 | C++ 基準與 cache/SIMD 分析報告 |
| [06 CPU 平行化、NUMA 與測試整合](weeks/week-06/README.md) | 量測單機 CPU 平行效率並用證據分辨運算與記憶體限制。 | 一台多 vCPU Linux VM；NUMA 不存在則做設計分析 | OpenMP 擴展曲線與 CPU 自動化成果 |
| [07 GPU 架構與 CUDA 從零](weeks/week-07/README.md) | 親寫第一個 CUDA kernel，理解執行模型、記憶體與同步。 | 一張 NVIDIA GPU | 含 CPU reference 與錯誤處理的 CUDA 向量加法 |
| [08 CUDA 記憶體與 kernel 調校](weeks/week-08/README.md) | 以正確性與量測支持 coalescing、shared memory 與 reduction 設計。 | 一張 NVIDIA GPU | 三個 CUDA A/B 實驗與可重現基準 |
| [09 Nsight 與 GPU 瓶頸診斷](weeks/week-09/README.md) | 以 timeline 和 kernel 指標區分傳輸、啟動、頻寬與計算限制。 | 一張 NVIDIA GPU；計數器權限依環境 | Nsight 診斷報告與一個受控調整 |
| [10 數學、NumPy 與 ML 從零](weeks/week-10/README.md) | 親手完成預測、loss、梯度與更新，不預設機器學習基礎。 | 一台 CPU VM | NumPy 線性模型與梯度檢查 |
| [11 PyTorch 與神經網路從零](weeks/week-11/README.md) | 親寫 tensor、autograd、Module 與完整訓練/驗證流程。 | CPU 起步，再使用單 GPU | 可在 CPU/GPU 訓練的 MLP 與 checkpoint |
| [12 ML 訓練效能 Profiling](weeks/week-12/README.md) | 拆解資料、搬移、forward/backward 與 optimizer 的成本。 | 一張 NVIDIA GPU | ML 基準、PyTorch trace 與瓶頸分析 |
| [13 ML 精度、記憶體與調校](weeks/week-13/README.md) | 以品質約束比較 AMP、累積與編譯，完成 ML 效能成果。 | 一張 GPU | 兩輪受控調校與 ML 完整報告 |
| [14 LLM 基礎與 Attention 實作](weeks/week-14/README.md) | 從 token 與機率開始親寫 causal attention，不預設 NLP 知識。 | CPU 起步，單 GPU 驗證 | tokenizer、小型 attention 與形狀測試 |
| [15 從零訓練小型 GPT](weeks/week-15/README.md) | 組裝 decoder Transformer 並完成真正的 next-token 訓練。 | 一張 GPU；小模型依顯存縮放 | 可恢復訓練的小型 GPT 與學習曲線 |
| [16 LLM 訓練 Profiling 與記憶體模型](weeks/week-16/README.md) | 量化 attention、MLP、optimizer、資料與 checkpoint 成本。 | 一張 GPU | LLM 基線與記憶體/時間分解報告 |
| [17 LLM 單卡調校與標準模型](weeks/week-17/README.md) | 比較 SDPA、activation checkpointing 與累積，轉移到標準 Transformer 實作。 | 一張 GPU，模型須在現有顯存內 | 三份 LLM 調校實驗與標準模型訓練驗證 |
| [18 跨節點 TCP 與網路效能](weeks/week-18/README.md) | 在兩台不同 CPU VM 建立可信網路基線與瓶頸診斷。 | 兩台不同 Linux CPU VM，同 zone 私有網路優先 | 雙主機 TCP 吞吐/延遲與系統觀察報告 |
| [19 MPI 跨節點平行計算](weeks/week-19/README.md) | 親寫 MPI 通訊與歸約並在兩台 CPU VM 驗證正確性和擴展。 | 兩台不同 CPU VM；Open MPI | 跨節點 MPI 程式、通訊曲線與擴展報告 |
| [20 Slurm 真實跨節點排程](weeks/week-20/README.md) | 建立或驗證最小兩節點 Slurm，能提交、綁定與診斷工作。 | 兩台 CPU worker VM；controller 可共用其中一台 | Slurm 作業、MPI 整合與失敗診斷紀錄 |
| [21 CPU Gloo 與跨節點 DDP](weeks/week-21/README.md) | 從 process group 到真實雙節點訓練，驗證梯度同步與資料切分。 | 兩台 CPU VM；PyTorch CPU/Gloo | 跨節點 DDP 正確性、吞吐與除錯報告 |
| [22 分散式系統與儲存調校](weeks/week-22/README.md) | 結合 CPU、網路、儲存與排程指標診斷真實工作。 | 兩台 CPU VM；單 GPU 可分時使用 | 兩個系統調校案例與診斷決策表 |
| [23 RDMA、NCCL 與多卡診斷設計](weeks/week-23/README.md) | 掌握必要原理與診斷流程，明確區分設計、模擬和硬體實測。 | CPU VM 做盤點；多 GPU/RDMA 實測皆選修 | RDMA/NCCL 原理問答、拓樸圖與補測計畫 |
| [24 四大成果整合與面試驗收](weeks/week-24/README.md) | 獨立重現四大能力成果，識別缺口並能處理陌生變化。 | 既有 CPU VM 與一張 GPU，按需分時 | 四份成果報告、重現入口與能力邊界清單 |

## 變更規則

改週目標、順序或必修範圍前，先提出具體 diff、職缺理由及影響，取得使用者明確同意再提交。修錯字、補說明或相容命令可直接修正，但不能藉此換課。24 週是固定課程結構；延長某日練習不改週次。
