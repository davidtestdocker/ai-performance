#!/usr/bin/env bash
# 在控制節點執行已編譯的熱擴散程式，取八秒程序 CPU 樣本並等待正確性結果。
# 只印出量測資訊；需先把 heat2d_cpu.cpp 編譯成 /tmp/heat2d_cpu。

set -e

# 沒有可執行檔就停止，避免 pidstat 量到錯誤的程序。
if [[ ! -x /tmp/heat2d_cpu ]]; then
    echo '缺少 /tmp/heat2d_cpu；請先編譯熱擴散程式。' >&2
    exit 1
fi

# & 讓工作在背景執行；$! 是剛啟動的程序編號，供 pidstat 精確選取。
/tmp/heat2d_cpu &
workload_pid=$!

# -u 選程序 CPU 指標，-p 指定工作程序；每秒取樣一次，共八筆。
pidstat -u -p "$workload_pid" 1 8

# 等工作完成並回傳其退出狀態；validation=FAIL 時腳本也會失敗。
wait "$workload_pid"
