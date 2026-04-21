# Binary Search: Expert Variants (二元搜尋：專家級變體與應用)

## I. Problem Statement & Nuances (題目與細節)
Binary search is more than just finding an index in a sorted array. It is a fundamental strategy for searching within any **Monotonic Function space**.
二元搜尋不僅僅是在排序陣列中尋找索引，它是在任何**單調函數空間**中進行搜尋的基礎策略。

**Nucleus Insights (核心觀點):**
- **The "Check" Function**: The key to expert-level BS is defining a boolean function `check(x)` that is monotonic (e.g., `false, false, true, true`). (專家級二元搜尋的關鍵在於定義一個單調的布林函式。)
- **Search on Answer**: Not searching for an input, but searching for the **minimal valid solution** in a range of possible answers. (不是搜尋輸入，是在可能的答案範圍中搜尋「最小有效解」。)
- **Precision (Float BS)**: Handling epsilon ($\epsilon$) precision in continuous search spaces. (處理連續搜尋空間中的精度問題。)

---

## II. Mechanical Deep-Dive: Boundary Conditions (底層原理：邊界條件)

The most common source of bugs in Binary Search is the **Infinite Loop** caused by incorrect mid-point calculation.
二元搜尋中最常見的 Bug 是錯誤的中點計算導致的**無限迴圈**。

### 1. The Template (Standard / 標準模板)
```go
left, right := 0, len(nums)-1
for left <= right {
    mid := left + (right - left) / 2 // Avoid overflow / 避免溢位
    if check(mid) {
        // ... adjust boundaries
    }
}
```

### 2. Search on Answer (The L5+ Secret / 專家級秘密)
Instead of searching `nums[]`, we search `[min_answer, max_answer]`.
我們不搜尋 `nums[]`，而是搜尋 `[最小可能解, 最大可能解]`。
Example: "Find the smallest capacity that allows shipping all items in D days."

---

## III. Quantitative Analysis Table (量化指標分析)

| Scenario (場景) | Time Complexity | Space Complexity | Iterations for $N=10^9$ |
|---|---|---|---|
| **Standard BS** | $O(\log N)$ | $O(1)$ | ~30 iterations |
| **Search on Answer** | $O(\text{SearchSpace} \times \text{CheckCost})$ | $O(1)$ | ~30-64 * Check |
| **Linear Search** | $O(N)$ | $O(1)$ | $1,000,000,000$ |

*Expert Note: $O(\log N)$ is so efficient that $N=2^{64}$ only takes 64 steps.*

---

## IV. Expert Variants & Challenges (專家級變體與挑戰)

| Variant (變體) | The Twist (挑戰點) | Strategy (策略) |
|---|---|---|
| **Rotated Sorted Array** | One half is always sorted. (其中一半始終是排序好的。) | Identify the sorted half and check if target is within it. |
| **Peak Index (Bitonic)** | Find the max in an array that increases then decreases. | If `mid < mid+1`, peak is on the right. |
| **Median of Two Sorted Arrays**| $O(\log(\min(M, N)))$ required. | Binary search on the shorter array's partition. |

---

## V. Code: Production Grade (Search on Answer - Shipping Capacity)

```go
// Find the minimal capacity to ship items within D days
// 尋找能在 D 天內運送完所有物品的最小容量
func ShipWithinDays(weights []int, D int) int {
    left, right := 0, 0
    for _, w := range weights {
        if w > left { left = w }
        right += w
    }

    result := right
    for left <= right {
        mid := left + (right-left)/2
        if canShip(weights, D, mid) {
            result = mid
            right = mid - 1 // Try smaller / 嘗試更小
        } else {
            left = mid + 1  // Need more capacity / 需要更大
        }
    }
    return result
}

func canShip(weights []int, D int, cap int) bool {
    days, current := 1, 0
    for _, w := range weights {
        if current + w > cap {
            days++
            current = w
        } else {
            current += w
        }
    }
    return days <= D
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Integer Overflow**: Using `(left + right) / 2` when $L+R > 2^{31}-1$. **Fix**: `left + (right-left)/2`. (當 $L+R$ 溢位時，中點計算會出錯。)
2. **Infinite Loop**: If the range doesn't shrink (e.g., `left = mid` and `left/right` are adjacent). (範圍未縮減時會陷入無限迴圈。)
3. **Non-monotonicity**: Attempting BS on a function that is not monotonic (has multiple peaks/valleys). (在非單調函數上嘗試二元搜尋。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Monotonic Function | 單調函數 | A function that is either non-decreasing or non-increasing. (始終遞增或始終遞減的函數。) |
| Search Space | 搜尋空間 | The range of all possible values for the answer. (答案所有可能的取值範圍。) |
| Lower Bound | 下界 | The first index $i$ where `nums[i] >= target`. (第一個大於或等於目標的索引。) |
| Upper Bound | 上界 | The first index $i$ where `nums[i] > target`. (第一個大於目標的索引。) |
