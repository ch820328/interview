# Heap / Priority Queue (優先佇列)

### 📌 核心概念
一棵 Complete Binary Tree (通常用陣列實作)，其中父節點的值總是大於/等於（Max Heap）或小於/等於（Min Heap）其子節點。

### 📌 適用情境 (何時該想到它？)
- 題目要求「Top K」最大、最小的元素。
- 需要不斷從不斷增加/減少的資料流中找出極值。
- Dijkstra's Algorithm (單源最短路徑) 的輔助結構。

### 📌 優缺點分析 (Trade-offs)
- **優點**：可以在 O(1) 的時間取得最大/最小值，並在 O(logN) 的時間插入或刪除元素。
- **缺點**：無法快速尋找「非極值」的元素 (需 O(N))；且只保證根節點是極值，左右子節點沒有嚴格排序。相比於排序整個陣列 O(NlogN)，維持一個 Size 為 K 的 Heap 只需要 O(NlogK)。

### 📌 語言特性實戰
- **Python**: 提供 `heapq` 模組，但預設只有 Min Heap。要模擬 Max Heap 時可以將數值加上負號 (`-val`)。
- **Go**: 必須自己定義一個 `type`，實作 `sort.Interface` (包含 `Len`, `Less`, `Swap`) 再加上 `Push` 與 `Pop`，總共五個方法，非常繁瑣。L4 面試時建議「口頭說明」可以自己實作，並問面試官能否假設有一個 `Heap` 可以用以專注演算法邏輯。
- **Rust**: 提供 `std::collections::BinaryHeap`，預設為 Max Heap。若需要 Min Heap 可以用 `std::cmp::Reverse` 包裝元素。

### 💻 經典模板與 Sample Code

#### 模板：Top K 元素 (Min Heap 以維護最大的 K 個元素)
如果要求 Top K 大的元素，維持一個 Size 為 K 的 Min Heap；如果新元素大於 Heap 頂端，就把頂端 pop 掉加入新元素。
**Python**:
```python
import heapq

def findKthLargest(nums: list[int], k: int) -> int:
    min_heap = []
    
    for num in nums:
        heapq.heappush(min_heap, num)
        # 只要長度大於 K，就把最小的踢掉，剩下的就會是前 K 大的元素
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    return min_heap[0] # Heap頂端就是第 K 大的元素
```


