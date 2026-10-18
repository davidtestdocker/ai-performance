"""在控制節點量測平方和計算與等待時間；只印出結果，不讀寫檔案。"""

from time import perf_counter, process_time, sleep


def main() -> None:
    """固定計算 500 萬項平方和，核對答案，並印出計算與等待的兩種時間。"""
    # 固定項數，讓每次執行的是同一份 CPU 工作。
    count = 5_000_000
    # 0² + 1² + ... + (count-1)² 的公式；用來檢查計時工作有算對。
    expected = count * (count - 1) * (2 * count - 1) // 6

    # perf_counter 量實際經過的 wall time；process_time 量本程式用掉的 CPU time。
    # 兩個起點都放在迴圈前，結束時間都放在迴圈後，避免把印出結果算進去。
    wall_start = perf_counter()
    cpu_start = process_time()
    total = 0
    for number in range(count):
        total += number * number
    cpu_seconds = process_time() - cpu_start
    wall_seconds = perf_counter() - wall_start

    # 答案不對就停止，避免把錯誤計算得到的速度當成有效結果。
    if total != expected:
        raise SystemExit(f"平方和錯誤：實際 {total}，預期 {expected}")
    print(f"平方和正確：{total}")
    print(f"CPU 計算：wall={wall_seconds:.6f}s cpu={cpu_seconds:.6f}s")

    # 等待半秒不做計算，用同樣兩種計時器觀察「經過時間」與「CPU 工作時間」的差別。
    wall_start = perf_counter()
    cpu_start = process_time()
    sleep(0.5)
    cpu_seconds = process_time() - cpu_start
    wall_seconds = perf_counter() - wall_start
    print(f"等待半秒：wall={wall_seconds:.6f}s cpu={cpu_seconds:.6f}s")


if __name__ == "__main__":
    # 直接執行這個檔案時才開始量測；匯入檔案不會自動跑工作。
    main()
