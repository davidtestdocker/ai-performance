# 鴻海 HPC AI 效能工程師：24 週固定實作課程

24 週 × 每週 5 個教學日，共 120 日。從 Linux 系統效能與計算機架構開始，Python、C/C++、CUDA、PyTorch、ML 與 LLM 從零親手實作。一般 Linux 指令入門不占課程週次。

**GitHub main 是唯一課綱基準。未經使用者同意，不改週次目標。** 全部進度重新開始；舊課綱和舊實作只存在 Git 歷史，不算本次完成或學員已會。

## 開始與續課

1. 讀 [PROGRESS.md](PROGRESS.md)，定位目前週、日與微步驟。
2. 讀 [固定 ROADMAP](curriculum/ROADMAP.md) 與該日教材。首次從 [W01D01](curriculum/weeks/week-01/day-01/README.md) 開始。
3. 教練一次只給一個小操作，收到真實輸出、判讀並確認理解後才往下。完整教材可預覽，但不能一次丟整天任務要求照做。
4. 每天完成精簡中文複習、兩題中文面試問答及驗收，才更新進度。

## 四項職缺能力與交付

| 能力 | 主要週次 | 最終作品 |
|---|---|---|
| A 自動化測試與數據分析 | 1–6、24 | runner、正確性/失敗分類、CSV、圖與回歸規則 |
| B ML 效能分析 | 7–13、24 | ML 訓練、CPU/GPU trace、資料與計算調校 |
| C LLM 訓練效能分析 | 14–17、24 | 自寫小 GPT、標準模型訓練、tokens/s/顯存/品質實驗 |
| D 分散式軟硬體調校 | 18–23、24 | 真實雙節點 TCP、MPI、Slurm、CPU DDP 與診斷設計 |

Python/C/C++ 與數學是上述工作的必要基礎，不宣稱每個練習或工具都由職缺原文明列。規劃依據是使用者提供的四大職責；尚未取得完整職缺原文，不保證涵蓋未提供條件或保證錄取。詳見[成果門檻與能力邊界](curriculum/OUTCOMES.md)。

## 設備與實作原則

- 最多一張 GPU：CUDA、Nsight、PyTorch、ML/LLM 訓練 profiling。
- 兩台小型 CPU VM：真實跨節點 TCP、MPI、Slurm、CPU Gloo/DDP；不同 VM 身分與兩端日誌是必要證據。
- RDMA 支援待盤點，與單 GPU quota 無直接關係；RDMA/NCCL 原理和診斷設計必修，多 GPU scaling、InfiniBand/RDMA 硬體實測選修。
- 不為日常練習要求租用 H4D 等大型機型，不重建無關 Kubernetes 平台，不以模擬冒充硬體實測。

[設備與限制](curriculum/EQUIPMENT.md)｜[帶練規則](curriculum/TEACHING.md)｜[量測規範](curriculum/MEASUREMENT.md)｜[官方參考](curriculum/REFERENCES.md)｜[代理規則](AGENTS.md)｜[完整檔案清單](FILES.md)

## 文件與學習成果分開

`curriculum/weeks/week-XX/README.md` 是每週目標及驗收，`day-YY/README.md` 是每日教材、微步驟、中文複習與兩題問答。實際開始後才建立 `labs/` 與 `evidence/`；本次只建立課程，不預填實測結果。檢查文件結構可執行 `python tools/validate_curriculum.py`，此檢查不代表 120 天實驗已通過。
