# Hash Table (雜湊表)

### 📌 核心概念
透過 Hash Function 將 Key 對應到陣列索引，實現平均 O(1) 的尋找、插入、刪除。

### 📌 適用情境 (何時該想到它？)
- 題目要求 O(1) 尋找某個元素是否存在。
- 需要統計頻率（Frequency Map）。
- 空間換取時間的典型手段。

### 📌 優缺點分析 (Trade-offs)
- **優點**：極致的尋找與更新速度。
- **缺點**：空間開銷大；最差情況（Hash Collision, 碰撞過多時）時間複雜度會退化至 O(N)；通常是無序的。

### 📌 語言特性實戰
- **Go**: map 是 un-ordered 的，遍歷的順序每次都不同。Go Map 並不保證並發安全，多 Goroutine 讀寫需加 `sync.RWMutex` 或用 `sync.Map`。
- **Rust**: 預設的 `HashMap` 使用安全的 Hash 演算法以防禦 HashDoS 攻擊，但效能稍微慢一點。
- **Python**: 字典 (`dict`) 在 Python 3.7+ 之後保證了插入順序。底層實作為高度優化的 Hash Table。

### 💻 經典模板與 Sample Code

#### 模板：Two Sum 變形 (利用 Hash Map 實作 O(N))
用空間換取時間的完美例子，一邊遍歷一遍存入 Map 檢查。
**Python**:
```python
def twoSum(nums: list[int], target: int) -> list[int]:
    num_map = {} # val -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
```

#### 模板：頻率統計 (Frequency Map)
**Python**:
```python
import collections

def topKFrequent(nums: list[int], k: int) -> list[int]:
    # 使用 collections.Counter 來快速完成頻率統計
    freq = collections.Counter(nums)
    
    # 或者手動實作：
    # freq = {}
    # for num in nums:
    #     freq[num] = freq.get(num, 0) + 1
        
    # 後續搭配 Heap 或是 Bucket Sort...
    return []
```
