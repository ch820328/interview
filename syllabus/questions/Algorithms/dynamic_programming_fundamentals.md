# Dynamic Programming: Expert Principles (動態規劃：專家級核心原理)

## I. Problem Statement & Nuances (題目與細節)
Dynamic Programming (DP) is often the most feared topic in technical interviews. It is an optimization method used to solve complex problems by breaking them down into simpler sub-problems.
動態規劃 (DP) 往往是技術面試中最令人恐懼的主題。它是一門透過將複雜問題分解為簡單子問題來求解的優化技術。

**Nucleus Insights (核心觀點):**
- **Overlapping Subproblems**: DP is only useful if you are solving the same sub-problem multiple times. (只有當您重複求解同一個子問題時，DP 才有意義。)
- **Optimal Substructure**: The optimal solution to the large problem can be constructed from optimal solutions of its sub-problems. (大問題的最佳解可以從子問題的最佳解中構建出來。)
- **State Definition**: The hardest part of DP is defining what $DP[i]$ actually represents. (DP 最難的部分在於定義 $DP[i]$ 到底是代表什麼。)

---

## II. Mechanical Deep-Dive: Top-Down vs. Bottom-Up (底層原理：由上而下與由下而上)

### 1. Memoization (Top-Down / 記憶化)
- **Concept**: Recursion with a cache. (帶有快取的遞迴。)
- **Pros**: Easy to implement from a brute-force approach. Only solves necessary sub-problems. (易於從暴力破解法轉化。僅求解必要的子問題。)

### 2. Tabulation (Bottom-Up / 表格法)
- **Concept**: Iteration using an array. (使用陣列的迭代。)
- **Pros**: Avoids recursion depth limits (Stack Overflow). Often allows for **Space Optimization**. (避免遞迴深度限制。通常支援**空間優化**。)

---

## III. Quantitative Analysis: Complexity Trade-offs (量化指標：複雜度權衡)

| Metric (指標) | Brute Force (Recursion) | Memoization (Top-Down) | Tabulation (Bottom-Up) |
|---|---|---|---|
| **Time Complexity** | $O(2^N)$ or $O(N!)$ | $O(\text{State Space} \times \text{Transitions})$ | Same as Memoization |
| **Space Complexity**| $O(N)$ (Stack) | $O(\text{State Space})$ | $O(\text{State Space})$ or **$O(1)$** |
| **Optimization** | None | Overlap detection | **State Compression** possible |

*Note: For many problems, Tabulation allows reducing space from $O(N)$ to $O(1)$ by only keeping the last few states.*

---

## IV. The "Expert" 4-Step DP Framework (專家級 4 步 DP 框架)

1. **Verify DP Property**: Check for overlapping subproblems. (確認是否存在重疊子問題。)
2. **Define State**: e.g., $DP[i][j]$ is the max profit using first $i$ items with capacity $j$. (定義狀態。)
3. **Relation (State Transition)**: $DP[i] = f(DP[i-1], DP[i-2], ...)$. (找出狀態轉移方程式。)
4. **Identify Base Cases**: e.g., $DP[0] = 1$. (確認基礎情況。)

---

## V. Code: Production Grade (Fibonacci Space Optimized / 費氏數列空間優化)

```go
package main

import "fmt"

// Expert: Space optimized to O(1)
// 專家級：空間優化至 O(1)
func Fibonacci(n int) int {
    if n <= 1 {
        return n
    }
    
    // We only need the last two states (我們只需要最後兩個狀態)
    prev2, prev1 := 0, 1
    
    for i := 2; i <= n; i++ {
        current := prev1 + prev2
        // Transition: Move the window forward
        prev2 = prev1
        prev1 = current
    }
    
    return prev1
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Stack Overflow**: Top-down recursion can crash for large $N$ (e.g., $N > 10^4$) if the recursion tree is deep. (當 $N$ 很大時，若遞迴樹過深，由上而下的方式會導致崩潰。)
2. **Incorrect Overlap**: If subproblems don't overlap, DP is just overhead. Use Divide & Conquer instead. (若子問題不重疊，DP 只是額外開銷，應使用分治法。)
3. **Invalid State Transition**: Missing a condition (e.g., ignoring a specific case) will lead to incorrect optimal solutions. (漏掉任何一個轉移條件都會導致解答錯誤。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| State Transition | 狀態轉移 | Equation governing the movement between subproblems. (規範子問題之間變化的方程式。) |
| Overlapping Subproblems | 重疊子問題 | Solving the same calculation multiple times. (多次執行相同的計算。) |
| Tabulation | 報表法 / 表格法 | Filling up an array/table to avoid recursion. (填充陣列或表格以避免遞迴。) |
| State Compression | 狀態壓縮 | Reducing the space needed to represent DP states. (縮減代表 DP 狀態所需空間的技術。) |
