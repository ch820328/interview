# Stack & Queue (堆疊與佇列)

### 📌 核心概念
- **Stack**: 後進先出 (LIFO)。
- **Queue**: 先進先出 (FIFO)。

### 📌 適用情境 (何時該想到它？)
- **Stack**: 具有「對稱性」、「配對性」或「最近相依性」的問題（如括號）。**Monotonic Stack (單調堆疊)** 更是解「尋找下一個更大/更小元素」的標準套路。
- **Queue**: 廣度優先搜尋 (BFS)、資料流的緩衝區。

### 📌 優缺點分析 (Trade-offs)
- **優點**：限制了存取方式，使得邏輯非常清晰。
- **缺點**：不支援隨機存取。

### 💻 經典模板與 Sample Code

#### 模板：Valid Parentheses (使用 Stack)
**Python**:
```python
def isValid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    
    for char in s:
        if char in mapping:
            # 取出堆疊頂部元素，若空則給個預設值
            top_element = stack.pop() if stack else '#'
            if mapping[char] != top_element:
                return False
        else:
            stack.append(char)
            
    return not stack # 必須全部清空才是合法的
```

#### 模板：Monotonic Stack (單調堆疊)
尋找陣列中每個元素的「下一個更大元素」(Next Greater Element)。堆疊裡存放的是「還沒找到答案的元素的 Index」。
**Python**:
```python
def nextGreaterElements(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack = [] # 儲存 index，且對應的值是遞減的 (維護單調遞減堆疊)
    
    for i in range(n):
        # 如果當前數字大於堆疊頂部記錄的數字，代表我們找到了頂部數字的 Next Greater
        while stack and nums[i] > nums[stack[-1]]:
            top_idx = stack.pop()
            res[top_idx] = nums[i] # 紀錄答案
        stack.append(i) # Push index
        
    return res
```
