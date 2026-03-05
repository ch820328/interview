# Dynamic Programming (動態規劃)

### 📌 核心概念
將大問題分解為互相重疊的子問題 (Overlapping Subproblems)，並把子問題的結果儲存起來 (Memoization / Tabulation)，以避免重複計算 (Optimal Substructure)。

### 📌 優缺點分析 (Trade-offs)
- **Top-Down (Memoization / 記憶化搜索)**：優點是程式碼好寫（就是遞迴加一個 HashMap 緩存），只計算需要的狀態；缺點是遞迴深度可能太深導致 Stack Overflow。
- **Bottom-Up (Tabulation / 製表)**：優點是執行速度快，且可以做到「空間壓縮」(Space Optimization)；缺點是比較難想到狀態轉移方程式。

### 💻 經典模板與 Sample Code

#### 模板 1：Top-Down DP (Memoization) - 以 Climbing Stairs 為例
**Python**:
```python
def climbStairs(n: int) -> int:
    memo = {}
    
    def dp(i: int) -> int:
        if i <= 2:
            return i
        if i in memo:
            return memo[i] # 命中快取，直接返回
            
        memo[i] = dp(i-1) + dp(i-2)
        return memo[i]
        
    return dp(n)
```

#### 模板 2：Bottom-Up DP (Tabulation 與空間壓縮) - 以 LIS 為例
Longest Increasing Subsequence 的 O(N²) 標準解。
**Python**:
```python
def lengthOfLIS(nums: list[int]) -> int:
    if not nums: return 0
    # dp[i] 代表「以 nums[i] 結尾的最長遞增子序列長度」
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[i] > nums[j]:
                dp[i] = max(dp[i], dp[j] + 1)
                
    return max(dp)
```

#### 模板 3：經典背包問題形式 (Coin Change)
求「最少硬幣數」，初始化為無限大 `float('inf')`。
**Python**:
```python
def coinChange(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != float('inf') else -1
```
