# 第 20 週：Slurm 真實跨節點排程

[固定課綱](../../ROADMAP.md)｜[進度](../../../PROGRESS.md)｜[帶練規則](../../TEACHING.md)

**固定目標：** 建立或驗證最小兩節點 Slurm，能提交、綁定與診斷工作。

**職缺對應：** D 分散式軟硬體調校；A 可信量測

**設備：** 兩台 CPU worker VM；controller 可共用其中一台

**先備：** 前 19 週必要驗收通過；新工具仍從最小例子開始。

| 日 | 主題 | 可觀察驗收 |
|---|---|---|
| [D01](day-01/README.md) | Slurm 元件與最小叢集 | 兩個真實節點可用，保存去密鑰配置與版本，未配置不得標完成。 |
| [D02](day-02/README.md) | sbatch、srun 與資源要求 | 作業配置與實際 hostname 相符，記 job ID、NodeList、exit code。 |
| [D03](day-03/README.md) | MPI 與 Slurm 整合 | 只有預期 ranks，兩節點、CPU 綁定與結果皆正確，保存 launcher 版本。 |
| [D04](day-04/README.md) | CPU binding 與 oversubscription | 說明 task/thread/core 映射，效能比較保持總工作量，恢復基線設定。 |
| [D05](day-05/README.md) | Slurm 故障與驗收 | 兩類失敗原因與修復有證據，正常 MPI 作業跨節點完成，記錄 accounting 是否啟用。 |

## 本週成果與通關

必交：**Slurm 作業、MPI 整合與失敗診斷紀錄**。五日驗收全部通過，且能獨立修改小輸入、重新執行與解釋結果，才可進下一週。

實驗報告需有問題、環境、原始資料、正確性、方法、結果與限制。不得要求湊出正向加速；未取得硬體計數器需明列替代證據。第 23 週以原理與診斷設計通關，硬體實測為選修。

[能力成果門檻](../../OUTCOMES.md)｜[官方參考](../../REFERENCES.md)
