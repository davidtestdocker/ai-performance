# 按階段學的必要觀念

此頁是概念索引。實際教學在當前階段先解釋必要概念，再操作，不一次背完所有名詞。

## 00 可信量測與系統觀察

wall time 是經過時間；CPU time 是程序實際用 CPU 的累計時間。程序 100% 通常約占一個邏輯 CPU，整機利用率還取決於 CPU 數量。利用率是線索，不能單獨證明瓶頸。

[練習與驗收](stage-00.md)

## 01 從零理解一次訓練

張量是有形狀的數值陣列；模型把輸入變成預測；loss 衡量誤差；backward 計算參數對誤差的梯度；optimizer 用梯度更新參數。

[練習與驗收](stage-01.md)

## 02 逐步建立 Python 量測工具

一次 run 是獨立執行；run 內每個 step 是相關的逐步樣本，兩者不能混成獨立重複。JSONL 一行一事件，原始資料保留後再產生摘要。

[練習與驗收](stage-02.md)

## 03 ML 訓練管線瓶頸診斷

完整訓練 step 包含取 batch、H2D、forward、loss、backward、optimizer。Profiler 用來定位時間路徑，帶 trace 的速度不直接當常態吞吐。

[練習與驗收](stage-03.md)

## 04 C／C++ 與 CUDA 資料移動

先理解 C 指標、長度與邊界，再理解 C++ 容器和 RAII 的資源生命週期。GPU kernel 由 thread／block 執行；連續存取、傳輸與啟動成本影響效能。

[練習與驗收](stage-04.md)

## 05 LLM 真正訓練與可信基準

先學 token 與 next-token label，再學 embedding、causal mask、attention、MLP。有效 batch＝microbatch×gradient accumulation×資料並行 world size；單卡最後一項為 1。

[練習與驗收](stage-05.md)

## 06 LLM 訓練效能調校

保持工作量可比；精度改變另列速度／數值取捨。Checkpointing 以重算換 activation 記憶體；SDPA 設定不等於實際 backend；compile 的啟動成本需另量。

[練習與驗收](stage-06.md)

## 07 分散式系統、儲存與 RDMA

Slurm 配資源，torchrun 啟動程序。CPU Gloo 驗證程序／collective 語意。DDP 同步梯度；FSDP 切分狀態並交換所需資料。RDMA 需要相容設備與完整路徑。

[練習與驗收](stage-07.md)

## 08 乾淨重現與面試交付

可重現性包含 host driver、容器 runtime、框架、模型、資料、設定與硬體；作品只能證明實際做過的範圍。

[練習與驗收](stage-08.md)
