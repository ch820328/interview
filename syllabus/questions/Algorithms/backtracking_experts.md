# Backtracking: Expert State-Space Analysis (回溯法：專家級狀態空間分析)

## I. Problem Statement & Nuances (題目與細節)
How do you efficiently explore all possible combinations or permutations of a set while avoiding unnecessary work? What is the difference between simple Recursion and "True" Backtracking?
如何在探索所有可能的組合或排列時，有效地避免不必要的計算？簡單的遞迴與「真正的」回溯法有何不同？

**Nucleus Insights (核心觀點):**
- **Implicit Graph**: Backtracking treats the problem as a traversal over an **Implicit State-Space Tree**. (回溯法將問題視為對「隱式狀態空間樹」的遍歷。)
- **Pruning (The Key)**: The power of backtracking comes from **Pruning**—eliminating branches that cannot possibly lead to a valid solution early. (回溯法的威力來自於「剪枝」——及早排除不可能產生解的分支。)
- **State Restoration**: The "Backtrack" step involves undoing the last choice to return the system to its previous state. (「回溯」步驟涉及撤銷上一步選擇，將系統恢復至先前的狀態。)

---

## II. Mechanical Deep-Dive: The Recursive Template (底層原理：遞迴模板)

Every backtracking problem follows a similar structural skeleton:
每個回溯問題都遵循相似的結構骨架：

1. **Choice**: Choose a path (e.g., pick a number). (選擇一條路徑。)
2. **Constraint Check**: Is this choice valid? (If no, **Prune**). (檢查約束，若無效則「剪枝」。)
3. **Goal Check**: Have we reached a complete solution? (是否達到目標。)
4. **Recurse**: Explore the next level. (進入下一層遞迴。)
5. **Backtrack**: Undo the choice (Reset state). (撤銷選擇，恢復狀態。)

---

## III. Quantitative Analysis: Complexity Risks (量化指標：複雜度風險)

| Category (分類) | Complexity (複雜度) | Scenario (場景) |
|---|---|---|
| **Subsets** | $O(2^N)$ | Power set of N elements. (N 個元素的冪集。) |
| **Permutations** | $O(N!)$ | Arrangements of N elements. (N 個元素的排列。) |
| **Sudoku / N-Queens** | $O(N^N)$ (Before pruning) | Constraint satisfaction problems. (約束補償問題。) |

---

## IV. Professional Pruning Strategies (專業剪枝策略)

| Strategy (策略) | Description (說明) | Outcome (結果) |
|---|---|---|
| **Feasibility Pruning** | Stop if the current path violates rules. (路徑違規即停止。) | Drastically reduces tree depth. |
| **Optimality Pruning** | Stop if the current path is already worse than the best found. (路徑已劣於目前最佳解即停止。) | Essential for "Branch and Bound". |
| **Memoized Backtracking** | Store results of sub-states to avoid re-calculating. (儲存子狀態結果。) | Transitions Backtracking into DP. |

---

## V. Code: Production Grade (Permutations w/ Backtracking in Go)

```go
package main

import "fmt"

func Permute(nums []int) [][]int {
    var result [][]int
    // State: Current permutation being built
    current := []int{}
    // Used map to track candidates (狀態追蹤)
    used := make(map[int]bool)

    var backtrack func()
    backtrack = func() {
        // Goal Check
        if len(current) == len(nums) {
            temp := make([]int, len(current))
            copy(temp, current)
            result = append(result, temp)
            return
        }

        for _, n := range nums {
            // Constraint Check (Pruning)
            if used[n] {
                continue
            }

            // 1. Choice
            used[n] = true
            current = append(current, n)

            // 2. Recurse
            backtrack()

            // 3. Backtrack (Undo state changes)
            // 撤銷選擇，恢復狀態
            current = current[:len(current)-1]
            delete(used, n)
        }
    }

    backtrack()
    return result
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Exponential Explosion**: Without pruning, the search space can grow beyond the limits of human time (Age of the Universe). (無剪枝的情況下，搜尋空間會發生爆炸性增長。)
2. **Mutable State Side-effects**: Forgetting to "Undo" a state change (e.g., not removing an element from a list) will corrupt the entire search tree. (忘記撤銷狀態變更會導致整棵搜尋樹出錯。)
3. **Deep Recursion**: Like DP, very deep backtracking can hit the stack limit. (過深的遞迴可能觸發棧溢位。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Pruning | 剪枝 | Removing branches of a decision tree that cannot lead to a solution. (移除決策樹中不可能產生解的分支。) |
| State-Space Tree | 狀態空間樹 | A tree representing all possible states of a problem. (代表問題所有可能狀態的樹。) |
| Constraint Satisfaction | 約束滿足 | Finding a solution that meets all specified rules. (尋找滿足所有規則的解。) |
| Branch and Bound | 分支定界 | An optimization of backtracking used for search problems. (回溯法的優化，用於搜尋問題。) |
