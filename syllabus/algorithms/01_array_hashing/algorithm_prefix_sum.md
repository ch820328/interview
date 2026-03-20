# Prefix Sum (前綴和)

### 📌 核心概念
預先計算陣列從開頭到當前索引的元素總和。公式：`sum(i, j) = prefixSum[j] - prefixSum[i-1]`。

### 📌 適用情境 (何時該想到它？)
- 題目頻繁要求計算陣列中「任意區間的和」。
- 題目提到「連續子陣列的和為 K」這類問題，結合 Hash Table 一起使用。

### 💻 經典模板與 Sample Code

#### 模板：Subarray Sum Equals K (前綴和 + Hash Table)
這是 Google L4 極度高頻的考題，將 O(N²) 暴力解優化到 O(N)。
**Python**:
```python
def subarraySum(nums: list[int], k: int) -> int:
    # count_map 紀錄前綴和出現的次數。
    # 重點：必須預先放入 {0: 1}，代表「不選任何元素」的前綴和為 0 發生過 1 次
    count_map = {0: 1} 
    current_sum = 0
    res = 0
    
    for num in nums:
        current_sum += num
        # 如果 current_sum - k 曾經出現過，代表存在一段子陣列的和為 k
        if (current_sum - k) in count_map:
            res += count_map[current_sum - k]
        
        # 將當前前綴和加入 map
        count_map[current_sum] = count_map.get(current_sum, 0) + 1
        
    return res
```
