# Two Pointers (雙指針)

### 📌 核心概念
使用兩個指標在陣列、字串或鏈結串列中移動，通常用來取代雙層迴圈。

### 📌 適用情境 (何時該想到它？)
- **相向指針 (頭尾向中間收斂)**：已排序陣列找兩數之和、判斷迴文、裝最多水的容器。當移動指標可以**明確排除掉某些不可能的狀況**時適用。
- **同向/快慢指針**：陣列去除重複元素、Linked List 找中點或判斷是否有環。

### 📌 優缺點分析 (Trade-offs)
- **優點**：極低的空間複雜度（通常是 O(1)），能將 O(N²) 的問題降維成 O(N)。
- **缺點**：對於未排序且不具遞增/遞減規律的集合通常無效（需要先 O(NlogN) 排序）。

### 💻 經典模板與 Sample Code

#### 模板：相向指針 (以 Two Sum II 為例)
**Python**:
```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1] # 題目常要求 1-indexed
        elif current_sum < target:
            left += 1  # 太小了，讓左邊變大
        else:
            right -= 1 # 太大了，讓右邊變小
    return [-1, -1]
```

#### 模板：快慢指針 (以 Remove Duplicates 為例)
**Python**:
```python
def removeDuplicates(nums: list[int]) -> int:
    if not nums: return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```
