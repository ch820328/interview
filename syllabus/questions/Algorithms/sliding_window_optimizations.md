# Sliding Window Optimizations: Expert Analysis (滑動窗口優化：專家級分析)

## I. Problem Statement & Nuances (題目與細節)
How do you process contiguous sub-arrays or sub-strings efficiently without redundant calculations? What distinguishes a "Fixed Window" from a "Variable Window" strategy?
如何有效率地處理連續子陣列或子字串，同時避免重複計算？「固定窗口」與「變動窗口」策略有何區別？

**Nucleus Insights (核心觀點):**
- **State Incrementalism**: Adding one element and removing one element should be $O(1)$ to maintain the window state. (新增一個元素並移除一個元素應為 $O(1)$，以維持窗口狀態。)
- **The "Two-Pointer" Relationship**: Sliding window is a specialized extension of the Two-Pointer technique where the area between pointers is the "State". (滑動窗口是雙指標技術的特殊延伸，指標間的區域即為「狀態」。)
- **Monotonic Property**: The window works best when the problem has monotonic properties (e.g., adding an element only increases the sum). (當問題具有單調屬性時，滑動窗口效果最佳。)

---

## II. Mechanical Deep-Dive: Window Mechanics (底層原理：窗口機制)

### 1. Fixed-Size Window (固定大小)
Used when the window size $K$ is known.
當窗口大小 $K$ 已知時使用。
- **Action**: Move `right` to $K$, then slide `left` and `right` together.

### 2. Variable-Size Window (動態大小)
Used to find the "Maximum" or "Minimum" window satisfying a condition.
用於尋找滿足條件的「最大」或「最小」窗口。
- **Expand**: Increment `right` until the condition is met. (增加 `right` 直到滿足條件。)
- **Shrink**: Increment `left` until the condition is no longer met (to find the minimum) or to restore validity. (增加 `left` 以尋找最小窗口或恢復有效性。)

---

## III. Quantitative Analysis Table (量化指標分析)

| Scenario (場景) | Naive Approach (暴力法) | Sliding Window (滑動窗口) | Optimization (優化點) |
|---|---|---|---|
| **Max Subarray Sum** | $O(N^2)$ | $O(N)$ | Avoids re-summing entire sub-array. |
| **Substring w/ K Unique** | $O(N^2)$ | $O(N)$ | Uses a HashMap to track character counts. |
| **Max in Slid. Window** | $O(N \times K)$ | **$O(N)$** | Uses a **Monotonic Deque** for $O(1)$ access. |

*Expert Note: Sliding window reduces the search space from $O(N^2)$ pairs to $O(N)$ linear passes.*

---

## IV. Professional Hybrid Techniques (專業混合技術)

| Technique (技術) | Auxiliary Structure | Common Use Case (場景) |
|---|---|---|
| **Window + HashMap** | `Map<byte, int>` | Substring problems with character constraints. |
| **Window + Deque** | `Deque<int>` | **Sliding Window Maximum** (Finding local peaks). |
| **Window + Two Sets** | `Multiset` / `Heaps` | **Sliding Window Median** (Maintaining order). |

---

## V. Code: Production Grade (Minimum Window Substring - Go)

```go
// Find the smallest substring in 's' that contains all characters in 't'
// 在 's' 中尋找包含 't' 所有字元的最短子字串
func MinWindow(s string, t string) string {
    targetMap := make(map[byte]int)
    for i := 0; i < len(t); i++ { targetMap[t[i]]++ }

    windowMap := make(map[byte]int)
    left, right, matchCount := 0, 0, 0
    minLen := len(s) + 1
    startIdx := 0

    for right < len(s) {
        char := s[right]
        right++
        
        // 1. Expand Window (擴張窗口)
        if count, ok := targetMap[char]; ok {
            windowMap[char]++
            if windowMap[char] == count {
                matchCount++
            }
        }

        // 2. Shrink Window if all targets matched (若滿足條件則收縮窗口)
        for matchCount == len(targetMap) {
            if right - left < minLen {
                minLen = right - left
                startIdx = left
            }
            
            dChar := s[left]
            left++
            if count, ok := targetMap[dChar]; ok {
                if windowMap[dChar] == count {
                    matchCount--
                }
                windowMap[dChar]--
            }
        }
    }

    if minLen > len(s) { return "" }
    return s[startIdx : startIdx+minLen]
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Non-Positive Values**: In problems like "Subarray Sum Equals K", if values can be negative, the monotonic property breaks, and you must use **Prefix Sums + HashMaps** instead. (若有負值，單調性被破壞，需改用前綴和。)
2. **Offline vs Online**: Sliding window is an "Online" algorithm that works perfectly for streaming data. (滑動窗口是「在線」演算法，非常適合串流數據。)
3. **Empty Source/Target**: Always handle `len == 0` to prevent indexing errors. (務必處理空輸入以防止索引錯誤。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Monotonic Deque | 單調雙端隊列 | A deque that keeps its elements in sorted order. (保持元素排序順序的雙端隊列。) |
| State | 狀態 | The information maintained for the current window. (當前窗口所維護的資訊。) |
| Shrink / Contract | 收縮 | Moving the left pointer to reduce the window size. (移動左指標以縮減窗口。) |
| Enlarge / Expand | 擴張 | Moving the right pointer to increase the window size. (移動右指標以增加窗口。) |
