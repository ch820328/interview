from typing import List

from typing import List

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix: return 0
        
        # 使用二維陣列 memo 通常比字典快，且初始化為 0 代表尚未計算
        rows, cols = len(matrix), len(matrix[0])
        memo = [[0] * cols for _ in range(rows)]
        
        def dfs(i, j):
            # 1. 檢查緩存：如果算過了，直接回傳
            if memo[i][j] != 0:
                return memo[i][j]
            
            # 2. 基本長度：自己這格算 1
            max_len = 1
            
            # 3. 探索鄰居：在「進去」之前就檢查合法性
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + dx, j + dy
                
                # 只有在範圍內且「嚴格遞增」時才遞迴
                if 0 <= ni < rows and 0 <= nj < cols and matrix[ni][nj] > matrix[i][j]:
                    max_len = max(max_len, 1 + dfs(ni, nj))
            
            # 4. 存入緩存
            memo[i][j] = max_len
            return max_len

        # 遍歷所有起點
        return max(dfs(r, c) for r in range(rows) for c in range(cols))


# --- Test harness (測試) ---
if __name__ == "__main__":
    sol = Solution()
    # Case 1: Increasing path [1, 2, 6, 9]
    print(sol.longestIncreasingPath([[9,9,4],[6,6,8],[2,1,1]]))  # Expected: 4
    # Case 2: Increasing path [3, 4, 5, 6]
    print(sol.longestIncreasingPath([[3,4,5],[3,2,6],[2,2,1]]))  # Expected: 4
    # Case 3: Single element
    print(sol.longestIncreasingPath([[1]]))  # Expected: 1
