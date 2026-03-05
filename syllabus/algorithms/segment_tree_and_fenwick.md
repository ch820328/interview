# Segment Tree & Fenwick Tree (線段樹與樹狀陣列)

### 📌 核心概念
在陣列頻繁「單點修改」(Point Update) 並且需要「區間查詢」(Range Query - 如區間加總、區間最大/小值) 的情境下使用。一般的前綴和 (Prefix Sum) 雖然查詢是 O(1)，但單點修改會導致其後的所有前綴和都需要更新，複雜度高達 O(N)。線段樹能將這兩個操作都壓在 O(logN)。

### 📌 適用情境 (何時該想到它？)
- 題目有大量且交替的**區間查詢 (Range Sum, Range Max/Min)** 與**單點/區間修改 (Update/Modify)**。
- 舉例：LeetCode 的 `Range Sum Query - Mutable`。
- 如果是不需要修改的區間查詢，用 Prefix Sum (O(1)) 即可；如果只有一開始更新區間最後查詢，用 Difference Array (差分陣列) 即可。必須是**連環變動**才需要這兩種樹。

### 📌 Trade-offs: Segment Tree vs Fenwick Tree (Binary Indexed Tree / BIT)
- **Segment Tree (線段樹)**:
  - **優點**：非常通用，不僅能求區間和，還能求區間最大、最小值，甚至 GCD 等複雜 Associative 操作。
  - **缺點**：程式碼很長、實作繁瑣，空間需求較大（通常開 4N 的陣列大小）。
- **Fenwick Tree (BIT)**:
  - **優點**：極致簡潔（大約 15 行 Code 完成），利用 `lowbit (x & -x)` 的特性，空間只需要 N+1，常數極小，速度極快。
  - **缺點**：功能受限，通常只能用來做「區間和 (Range Sum)」或頻率統計，難以實作區間最大/最小值查詢。

### 💻 經典模板與 Sample Code

#### 模板 1：Segment Tree (陣列遞迴版)
適用於任何符合結合律的運算 (這裡以求區間和為例)。
**Python**:
```python
class SegmentTree:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        # 開 4 倍大小通常足以涵蓋所有節點
        self.tree = [0] * (4 * self.n)
        if self.n > 0:
            self._build(nums, 0, 0, self.n - 1)
            
    def _build(self, nums: list[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = nums[start]
            return
        mid = start + (end - start) // 2
        left_node = 2 * node + 1
        right_node = 2 * node + 2
        
        self._build(nums, left_node, start, mid)
        self._build(nums, right_node, mid + 1, end)
        
        # 這裡決定這棵線段樹是求和、求Max還是求Min
        self.tree[node] = self.tree[left_node] + self.tree[right_node]
        
    def update(self, index: int, val: int) -> None:
        def _update(node: int, start: int, end: int):
            if start == end: # 找到葉節點
                self.tree[node] = val
                return
            mid = start + (end - start) // 2
            left_node = 2 * node + 1
            right_node = 2 * node + 2
            
            # 判斷目標 index 在哪半邊
            if index <= mid:
                _update(left_node, start, mid)
            else:
                _update(right_node, mid + 1, end)
                
            # 子節點更新後，向上更新父節點
            self.tree[node] = self.tree[left_node] + self.tree[right_node]
            
        if self.n > 0:
            _update(0, 0, self.n - 1)
            
    def query(self, L: int, R: int) -> int:
        def _query(node: int, start: int, end: int, l: int, r: int) -> int:
            if r < start or l > end: # 區間完全不重疊
                return 0
            if l <= start and end <= r: # 節點區間完全被包含在查詢區間內
                return self.tree[node]
                
            mid = start + (end - start) // 2
            left_node = 2 * node + 1
            right_node = 2 * node + 2
            
            # 將查詢拆分到左右子樹
            res_left = _query(left_node, start, mid, l, r)
            res_right = _query(right_node, mid + 1, end, l, r)
            return res_left + res_right
            
        if self.n > 0:
            return _query(0, 0, self.n - 1, L, R)
        return 0
```

#### 模板 2：Fenwick Tree (BIT) - L4 會被視為極致優化亮點的版本
因為實作簡潔，能在面試的白板或線上編輯器光速敲完，是解 Range Sum Query Mutable 的神兵利器。**必須注意 BIT 通常內部是 1-indexed。**
**Python**:
```python
class FenwickTree:
    def __init__(self, size: int):
        # BIT 是 1-indexed，所以需要 size + 1
        self.tree = [0] * (size + 1)
        
    # lowbit 操作：取得最右邊的 1 所代表的值 (例如 1010 -> 0010 -> 2)
    def _lowbit(self, i: int) -> int:
        return i & -i
        
    # 單點更新：對 index i 增加 delta (注意是增加的量，不是直接取代成 delta)
    def add(self, i: int, delta: int) -> None:
        while i < len(self.tree):
            self.tree[i] += delta
            i += self._lowbit(i)
            
    # 前綴和查詢：計算第 1 項到第 i 項的總和
    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= self._lowbit(i)
        return s
        
    # 區間和查詢 [left, right] (1-indexed 的區間)
    def range_query(self, left: int, right: int) -> int:
        return self.query(right) - self.query(left - 1)
```
