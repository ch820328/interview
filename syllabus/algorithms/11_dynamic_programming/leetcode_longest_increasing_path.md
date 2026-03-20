# Longest Increasing Path in a Matrix (矩陣中的最長遞增路徑)

## Problem Statement (題目敘述)
Given an `m x n` integers `matrix`, return the length of the longest increasing path in `matrix`. From each cell, you can move in four directions (up, down, left, right). Diagonal moves and boundary wrap-arounds are not allowed.

給定一個 `m x n` 的整數矩陣 `matrix`，回傳其最長遞增路徑的長度。在每個儲存格中，你可以向四個方向（上、下、左、右）移動。不允許斜向移動或超出邊界。

## Constraints (限制條件)
- `m == matrix.length`
- `n == matrix[i].length`
- `1 <= m, n <= 200`
- `0 <= matrix[i][j] <= 2^31 - 1`

## Clarification Q&A (澄清問答)
- **Q: Does "increasing" mean strictly increasing? (遞增是指嚴格遞增嗎？)**
  - A: Yes, equal values are not valid. (是的，數值相等不列入路徑。)
- **Q: Can the path start from any cell? (路徑可以從任何格子開始嗎？)**
  - A: Yes. (是的。)
- **Q: What should be returned? (應回傳什麼？)**
  - A: The integer length of the path. (路徑的整數長度。)

## Brute Force vs Optimal Comparison (暴力法與優化解比較)

| Feature (特性) | Brute Force (暴力法) | Optimal (DFS + Memoization) |
|---|---|---|
| Approach (方法) | DFS for every cell (遍歷所有點 DFS) | DFS with caching (帶快取的 DFS) |
| Time Complexity (時間複雜度) | $O(4^{mn})$ | $O(m \times n)$ |
| Space Complexity (空間複雜度) | $O(mn)$ recursion depth (遞迴深度) | $O(m \times n)$ memo table (緩存表) |

## Python Code Sample (Python 範例程式)
```python
from typing import List

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0
            
        rows, cols = len(matrix), len(matrix[0])
        # memo[i][j] stores the LIP starting from (i, j)
        # memo[i][j] 儲存從 (i, j) 出發的最長遞增路徑長度
        memo = [[0] * cols for _ in range(rows)]
        
        def dfs(i: int, j: int) -> int:
            if memo[i][j] != 0:
                return memo[i][j]
            
            # Initial length is 1 (the cell itself)
            # 初始長度為 1 (包含自身)
            res = 1
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + dx, j + dy
                if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] > matrix[i][j]:
                    res = max(res, 1 + dfs(ni, nj))
            
            memo[i][j] = res
            return res
            
        return max(dfs(r, c) for r in range(rows) for c in range(cols))

# --- Test harness (測試) ---
if __name__ == "__main__":
    sol = Solution()
    # Test Case 1
    print(sol.longestIncreasingPath([[9,9,4],[6,6,8],[2,1,1]]))  # Expected: 4
    # Test Case 2
    print(sol.longestIncreasingPath([[3,4,5],[3,2,6],[2,2,1]]))  # Expected: 4
    # Test Case 3
    print(sol.longestIncreasingPath([[1]]))  # Expected: 1
```

## Step-by-Step Dry Run (逐步執行推導)
Using Example 1: `[[9,9,4],[6,6,8],[2,1,1]]`

| Step (步驟) | Cell (格子) | Action (行動) | Memo Update (緩存更新) |
|---|---|---|---|
| 1 | (0, 0) | Value 9, no larger neighbors. (值 9，無更大鄰居) | `memo[0][0] = 1` |
| 2 | (0, 2) | Value 4, goes to (1, 2). (值 4，走向 (1, 2)) | `memo[0][2] = 2` |
| 3 | (2, 1) | Value 1, chain: 1 -> 2 -> 6 -> 9. (值 1，路徑鏈 1-2-6-9) | `memo[2][1] = 4` |

## Common Bugs (常見錯誤)
| Bug (錯誤) | Mitigation (預防措施) |
|---|---|
| Missing boundary check (漏掉邊界檢查) | Always check `0 <= ni < rows` and `0 <= nj < cols`. (務必檢查索引範圍。) |
| Forgetting to add 1 in recursion (遞迴時忘記加 1) | Ensure `1 + dfs(ni, nj)` is used. (確保使用 1 + 子問題結果。) |
| Cycle handling (環節處理) | "Strictly increasing" prevents cycles, but memoization is key for efficiency. (「嚴格遞增」可防止無限循環，但記憶化是效能關鍵。) |

## Evaluation Rubric (評估量表)
1. **Communication (溝通):** Perfect. Clarified constraints before starting. (優異。開始前即釐清限制。)
2. **Problem Solving (問題解決):** Optimal approach derived quickly. (優異。迅速導出最佳解。)
3. **Coding Quality (程式品質):** Clean, standard Python implementation. (優異。程式碼乾淨且標準。)
4. **Follow-ups (追問):** Excellent discussion on Topological Sort and Distributed Systems. (優異。對拓撲排序與分散式系統有深入探討。)

## Actionable Corrections (行動修復建議)
- The candidate can explore **Topological Sort (Kahn's Algorithm)** as an iterative alternative for extreme recursion depths.
- 候選人可以進一步研究 **拓撲排序 (Kahn 演算法)**，作為在極端遞迴深度下的迭代替代方案。

## Technical Term Dictionary (技術術語字典)
| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| DFS | 深度優先搜尋 | Tracing paths as far as possible before backtracking. (在回溯前盡可能深入追蹤路徑。) |
| Memoization | 記憶化 | Storing the results of expensive function calls. (儲存高效率函數呼叫的結果。) |
| DAG | 有向無環圖 | A directed graph with no cycles. (沒有迴圈的有向圖。) |
| Topological Sort | 拓撲排序 | Linear ordering of vertices such that for every directed edge uv, u comes before v. (頂點的線性排序，使得所有有向邊都指向後方。) |
| Kahn's Algorithm | Kahn 演算法 | An algorithm for topological sorting. (用於拓撲排序的演算法。) |
