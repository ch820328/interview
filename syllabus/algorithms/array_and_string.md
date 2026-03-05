# Array & String (陣列與字串)

### 📌 核心概念
陣列是連續的記憶體區塊，優勢是 O(1) 的隨機存取；缺點是插入與刪除需要 O(N) 以移動其他元素。

### 📌 適用情境 (何時該想到它？)
- 題目要求 **In-place** 操作（空間複雜度 O(1)）。
- 尋找連續的一段子陣列。
- 需要預先分配固定大小的記憶體來優化效能。

### 📌 優缺點分析 (Trade-offs)
- **優點**：Cache-friendly（因為記憶體連續），讀取速度極快。
- **缺點**：插入/刪除成本高。

### 📌 語言特性實戰 (Go / Rust / Python)
- **Go**: 需清楚 `Slice` 與 `Array` 的差異，特別是 `append` 導致容量 (Capacity) 擴容時，底層會發生重新分配與複製（O(N)）。建議使用 `make([]int, 0, capacity)` 預先分配空間。
- **Rust**: 嚴格的 Borrow Checker。要在 In-place 交換元素時，需善用 `slice::swap`。
- **Python**: 字串是 Immutable（不可變）的，每次拼接 `s += "a"` 都會產生新物件。應善用 `"".join(list)` 來優化。

### 💻 經典模板與 Sample Code

#### 模板：In-place 字串反轉 (Two Pointers)
**Python**:
```python
def reverseString(s: list[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        # In-place 交換，Python 語法糖
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```


