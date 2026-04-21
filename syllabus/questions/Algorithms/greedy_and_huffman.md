# Greedy Algorithms: The Expert Choice Strategy (貪婪演算法：專家級選擇策略)

## I. Problem Statement & Nuances (題目與細節)
When can you make a local optimal choice and guarantee it leads to a global optimum? Why are Greedy algorithms faster but riskier than Dynamic Programming?
何時可以做出局部最優選擇，並保證其導向全域最優解？為什麼貪婪演算法比動態規劃更快，但風險也更高？

**Nucleus Insights (核心觀點):**
- **The Greedy Choice Property**: A global optimum can be reached by making a locally optimal choice without looking back. (無需回頭，透過局部最優選擇即可達到全域最優。)
- **Optimal Substructure**: Like DP, a greedy solution depends on the sub-problems also having optimal solutions. (與 DP 相同，貪婪解法依賴於子問題也具有最佳解。)
- **The Proof Burden**: Unlike DP (which guarantees optimality via brute-force + cache), Greedy requires a **proof** (usually by contradiction or exchange argument) to be verified. (貪婪演算法需要數學證明來驗證其正確性。)

---

## II. Mechanical Deep-Dive: Common Greedy Archetypes (底層原理：常見貪婪模式)

### 1. Interval Scheduling (區間調度)
- **Problem**: Given $N$ tasks, find the maximum number you can perform without overlap.
- **Expert Strategy**: Always pick the task that **finishes earliest**. This leaves the maximum room for future tasks. (始終選擇結束時間最早的任務。)

### 2. Fractional Knapsack (部分背包)
- **Problem**: Can take fractions of items with weight/value.
- **Expert Strategy**: Sort by **Value-to-Weight Ratio**. (依據價值重量比進行排序。)

### 3. Huffman Coding (霍夫曼編碼)
- **Problem**: Minimize average code length for data compression.
- **Expert Strategy**: Always merge the two nodes with the **lowest frequency**. (始終合併頻率最低的兩個節點。)

---

## III. Quantitative Analysis: Greedy vs. DP (量化指標對比)

| Feature (特性) | Greedy Algorithms | Dynamic Programming |
|---|---|---|
| **Mechanism** | Best choice *now*. | Considers *all* future choices. |
| **Time Complexity** | Usually $O(N \log N)$ (due to sorting). | $O(N^2)$ or $O(N \times K)$. |
| **Optimality** | Needs proof. (需證明。) | Guaranteed correct. (保證正確。) |
| **Speed** | Extremely High. | Moderate. |

*Expert Note: If a problem has the Greedy Property, DO NOT use DP. The $O(N)$ or $O(N \log N)$ gain is critical for performance infra.*

---

## IV. Professional Use Cases (專業使用場景)

| Use Case (場景) | Algorithm / Strategy | Why? (為什麼？) |
|---|---|---|
| **Request Throttling** | Token Bucket / Leaky Bucket. | Simplest greedy way to manage flow. |
| **Task Priority** | Shortest Job First (SJF). | Minimizes average waiting time. |
| **Network Routing** | Spanning Tree Protocol (STP). | Greedy cycles elimination. |

---

## V. Code: Production Grade (Interval Scheduling in Go)

```go
package main

import (
    "sort"
)

type Interval struct {
    Start, End int
}

// MaxIntervals: Find max non-overlapping intervals
func MaxIntervals(intervals []Interval) int {
    if len(intervals) == 0 { return 0 }

    // 1. Sort by End Time (專家級核心：依據結束時間排序)
    sort.Slice(intervals, func(i, j int) bool {
        return intervals[i].End < intervals[j].End
    })

    count := 1
    lastFinish := intervals[0].End

    for i := 1; i < len(intervals); i++ {
        // 2. Greedy Choice: Take if it doesn't overlap
        if intervals[i].Start >= lastFinish {
            count++
            lastFinish = intervals[i].End
        }
    }

    return count
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Greedy Trap**: If the local best choice ruins future possibilities (e.g., 0/1 Knapsack), Greedy will fail. (若局部選擇破壞了未來可能性，貪婪演算法將失效。)
2. **Incorrect Sorting**: Choosing the wrong criteria (e.g., sorting by start time instead of end time) leads to sub-optimal results. (選擇錯誤的排序基準會導致解法出錯。)
3. **Empty/Single Inputs**: Always handle boundary task sets. (處理空的或單一的任務集合。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Greedy Choice | 貪婪選擇 | Making the decision that looks best at the moment. (做出當下看來最好的決定。) |
| Exchange Argument | 交換論證 | A technique to prove greedy optimality by swapping elements. (透過交換元素來證明貪婪最佳性的技巧。) |
| Kruskal's Algorithm | 庫斯克演算法 | A greedy algorithm to find a Minimum Spanning Tree. (尋找最小生成樹的貪婪演算法。) |
| Matroid Theory | 擬陣理論 | A mathematical framework that guarantees greedy works for certain structures. (確保貪婪法在某些結構下可行的數學框架。) |
