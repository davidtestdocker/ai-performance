"""以可核對答案的 CPU 工作比較 wall time 與 CPU time。"""

from time import perf_counter, process_time, sleep


def main() -> None:
    """計算平方和、核對答案，並量測計算及等待的時間。"""
    count = 5_000_000
    expected = count * (count - 1) * (2 * count - 1) // 6

    wall_start = perf_counter()
    cpu_start = process_time()
    total = 0
    for number in range(count):
        total += number * number
    cpu_seconds = process_time() - cpu_start
    wall_seconds = perf_counter() - wall_start

    if total != expected:
        raise SystemExit(f"平方和錯誤：實際 {total}，預期 {expected}")
    print(f"平方和正確：{total}")
    print(f"CPU 計算：wall={wall_seconds:.6f}s cpu={cpu_seconds:.6f}s")

    wall_start = perf_counter()
    cpu_start = process_time()
    sleep(0.5)
    cpu_seconds = process_time() - cpu_start
    wall_seconds = perf_counter() - wall_start
    print(f"等待半秒：wall={wall_seconds:.6f}s cpu={cpu_seconds:.6f}s")


if __name__ == "__main__":
    main()
