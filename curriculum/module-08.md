# 模組 08：分散式 collective 與擴展判斷

[路線](ROADMAP.md)｜目標：能驗證 rank 分工正確、量測同步成本，並用有限的實測資料辨認擴展推估的邊界。

[觀念講義](CONCEPTS.md)第 08 節｜[作品成果](OUTCOMES.md)

## 學習大綱

rank/collective 語意 → 單機正確性 → 跨節點訊息大小掃描 → 運算／通訊分解 → 假設清楚的擴展模型。

## 先理解

rank、world size、broadcast、all-reduce、啟動成本、同步點、運算／通訊比。CPU Gloo/MPI 與 GPU NCCL 的執行路徑不同，不能互換效能數字。PyTorch 建議 CPU 工作採 Gloo。[PyTorch 分散式文件](https://docs.pytorch.org/docs/stable/distributed.html)

## 實作

1. 先用一台主機兩個 CPU process 寫 `all_reduce`／broadcast 正確性案例，和單程序答案核對；記錄 rank、hostname、輸入、輸出。
2. 用兩台獨立 CPU 主機跑相同程式，掃描 4 KiB 到能承受的較大訊息；做暖機與獨立重複，記錄每 rank 時間、有效頻寬和 CPU 使用率。對照模組 07 的 TCP 量測，解釋 collective 額外成本。
3. 選一個簡單的 CPU 分散式訓練或梯度平均工作，測量 compute、等待與同步所占時間；只在能保持相同工作量時比較設定。
4. 用模組 05 的單卡 compute 時間及本模組 CPU 通訊資料畫敏感度圖；明確寫出它只是架構估算，並列出要做多 GPU 驗證還缺什麼硬體與指標。

## 做完留下的成果

跨節點 rank 的不同 hostname、正確答案、訊息大小曲線、與 TCP 基線的差異解釋，以及「已測／推估／未測」表。單主機多 process 先作功能預演，跨節點結果仍需實測。
