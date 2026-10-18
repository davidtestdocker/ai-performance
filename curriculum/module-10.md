# 模組 10：RDMA 架構與故障診斷

[路線](ROADMAP.md)｜目標：能解釋 RDMA 與 TCP 的資料路徑差異，提出在有硬體時可執行的驗證；不將概念學習寫成 RDMA 實測。

[觀念講義](CONCEPTS.md)第 10 節｜[作品成果](OUTCOMES.md)

## 學習大綱

RDMA 與 TCP 資料路徑 → verbs 物件 → RoCE/InfiniBand 設備前提 → 錯誤與壅塞計數器 → 硬體條件式診斷。

## 先理解

RDMA memory registration、queue pair、work request、completion queue、InfiniBand、RoCE、PFC、ECN、CNP、NIC/error counters。畫出 CPU TCP 傳輸與 RDMA 傳輸路徑，標明資料複製、kernel 參與和網路設備前提。RoCE 問題可能與壅塞控制或 lossless fabric 設定相關，不能只看連線是否通。[NCCL 網路疑難排解](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/networking_troubleshooting.html)

## 實作

1. 檢查目前 NIC、driver、`rdma link`／`ibv_devinfo` 是否顯示可用 RDMA 裝置；記錄「無設備」也是有效盤點結果。
2. 依模組 07 的 TCP 實測，寫一份哪些瓶頸可能被 RDMA 改變、哪些仍由應用、儲存或網路容量決定的假設表；任何性能數字都標示來源與假設。
3. 設計 RDMA 有硬體時的 smoke test、`rping` 或 perftest 吞吐／延遲矩陣、NIC errors、PFC/ECN/CNP 等計數器和故障排查順序。若真的有兩台相容主機才執行並保存原始結果。
4. 設計未來 NCCL 多 GPU 實驗所需的 GPU/NIC 拓撲與量測條件；一張 GPU 只能提供設計，不能產生多 GPU 結果。

## 做完留下的成果

RDMA 與 TCP 架構圖、設備盤點、可執行的診斷 runbook、已測／未測清單。概念與診斷設計可完成；「RDMA 效能實測」單獨列為需設備的條件式成果。
