# 可信量測與證據格式

所有效能實驗先驗正確性，再量速度。不要求固定加速百分比，不刪除失敗或負結果。

## 每次 run 必記

run_id、時間/時區、source commit、主機/VM 身分、OS/kernel、CPU/GPU/記憶體、driver/toolkit、函式庫版本、輸入來源與雜湊、seed、完整命令、dtype、shape、batch、sequence、ranks/threads、計時範圍、warmup/repeats、退出碼與 stderr。沒有的欄位記不適用或未知，不能猜測。

原始結果與摘要分離。小型 CSV/JSON 可進 Git；大型 trace/資料/權重存外部位置，提交雜湊、大小、重建命令與摘要，不提交密鑰或私人資料。

## 正確性

CPU/CUDA 逐元素對照 reference，涵蓋 0（適用時）、1、非整除長度及不同數值尺度；浮點用事先合理定義的 atol/rtol。ML/LLM 檢查 shape、標籤對齊、梯度、參數更新、train/validation 與資料洩漏；loss 有限或總和相同不是充分證據。DDP 對照相同 global batch 的單程序更新。

## 計時與比較

區分冷啟動、穩態、純 kernel 和端到端。CPU 用單調時鐘；GPU events 和同步 wall time 明確分開。正式吞吐不開 profiler，trace 單獨擷取。一般效能組至少五次獨立短跑，TCP 依日教材雙向各三次；尾延遲需更充分樣本並寫算法。統計列 n、中位數、分布/範圍與失敗率。

A/B 固定輸入、硬體、品質口徑與有效工作，交錯順序並一次改一項。AMP 等精度變更另列品質取捨；不同序列/batch 的容量實驗不能宣稱相同工作量加速。速度未超出波動時寫證據不足，不硬下結論。

## 報告骨架

問題 → 基準與設定 → 正確性 → 假說 → 單一變因 → 原始數據與圖 → 判讀 → 限制/回退/下一步。圖含單位、樣本量與生成方式。跨節點必附兩台 VM 身分、rank placement、兩端日誌與 launcher；雲端 VM 的不同 instance 不保證不同物理宿主，限制應揭露。
