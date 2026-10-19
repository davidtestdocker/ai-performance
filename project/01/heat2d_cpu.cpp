// 固定大小的二維熱擴散工作：在控制節點執行，用來觀察運算期間的 CPU 活動。
// 中央熱源與更新次數固定；結束時核對總熱量並印出計算時間，不讀寫資料檔。

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <vector>

namespace {
constexpr int kSide = 1024;
constexpr int kSteps = 3000;
constexpr double kExpectedSum = 65536.0;
constexpr double kAllowedError = 0.5;
}

// 在 cells 中建立中央 256×256 的熱源；其餘方格維持零，總熱量應為 65536。
void initialize(std::vector<float>& cells) {
    const int first = 3 * kSide / 8;
    const int last = 5 * kSide / 8;
    for (int y = first; y < last; ++y) {
        for (int x = first; x < last; ++x) {
            cells[static_cast<size_t>(y) * kSide + x] = 1.0f;
        }
    }
}

// 從 input 的上下左右鄰點計算下一輪，寫入 output；外圈保持零。
void advance(const float* input, float* output) {
    for (int y = 1; y < kSide - 1; ++y) {
        for (int x = 1; x < kSide - 1; ++x) {
            const size_t at = static_cast<size_t>(y) * kSide + x;
            const float neighbors =
                input[at - 1] + input[at + 1] + input[at - kSide] + input[at + kSide];
            output[at] = input[at] + 0.2f * (neighbors - 4.0f * input[at]);
        }
    }
}

// 執行固定工作並核對總熱量；通過回傳 0，結果錯誤回傳 1。
int main() {
    const size_t count = static_cast<size_t>(kSide) * kSide;
    std::vector<float> current(count, 0.0f);
    std::vector<float> next(count, 0.0f);
    initialize(current);

    const auto start = std::chrono::steady_clock::now();
    for (int step = 0; step < kSteps; ++step) {
        advance(current.data(), next.data());
        std::swap(current, next);
    }
    const auto finish = std::chrono::steady_clock::now();

    double sum = 0.0;
    for (const float cell : current) {
        sum += cell;
    }
    const double error = std::abs(sum - kExpectedSum);
    const bool passed = std::isfinite(sum) && error <= kAllowedError;
    const double elapsed_seconds =
        std::chrono::duration<double>(finish - start).count();
    std::printf("grid=%dx%d steps=%d\n", kSide, kSide, kSteps);
    std::printf("sum=%.6f expected=%.6f abs_error=%.6f\n", sum, kExpectedSum, error);
    std::printf("compute_seconds=%.6f validation=%s\n", elapsed_seconds,
                passed ? "PASS" : "FAIL");
    return passed ? 0 : 1;
}
