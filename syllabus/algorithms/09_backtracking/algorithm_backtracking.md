# Backtracking (回溯法)

### 📌 核心概念
一種透過「暴力嘗試」尋找所有可能解的方法。通常用遞迴實作。本質上是在一棵決策樹 (Decision Tree) 上做 DFS 遍歷，如果走到死胡同就不斷返回上一層（回溯）。

### 📌 核心技巧與 L4 要求
1. **Choose (選擇)**：把元素加進當前的狀態路徑。
2. **Explore (深入遞迴)**：進入下一層。
3. **Un-choose (撤銷選擇)**：將元素移出路徑 (這就是 **回溯**)，確保上一層能繼續嘗試下一個選項。

在 L4 面試中，遇到 Backtracking 問題時，最好能主動向面試官提到 **Pruning (剪枝)**。

### 💻 經典模板與 Sample Code

#### 模板：Backtracking 通用框架 (以 Permutations 為例)
**Python**:
```python
def permute(nums: list[int]) -> list[list[int]]:
    res = []
    
    def backtrack(path: list[int], used: list[bool]):
        # Base case: 找到一組完整解
        if len(path) == len(nums):
            res.append(path[:]) # 必須拷貝一份 path，因為 path 會隨著遞迴不斷修改
            return
            
        for i in range(len(nums)):
            if used[i]:
                continue
            
            # 1. 選擇 (Choose)
            used[i] = True
            path.append(nums[i])
            
            # 2. 深入搜索 (Explore)
            backtrack(path, used)
            
            # 3. 撤銷選擇 (Un-choose / Backtrack)
            path.pop()
            used[i] = False
            
    backtrack([], [False] * len(nums))
    return res
```
