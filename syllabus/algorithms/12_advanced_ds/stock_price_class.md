# Coding Interview: Stock Price Fluctuations (股票價格波動)

**Topic / 主題:** Hash Map & Heap (Lazy Removal) / 哈希表與堆疊 (延遲刪除)
**Difficulty / 難度:** Medium (LeetCode 2034)
**Target Level / 目標等級:** Google L4
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-10

---

## 1. Problem Statement (題目)

**English:**
Implement a `StockPrice` class that supports updating stock prices at specific timestamps and querying the current, maximum, and minimum prices. Updates for the same timestamp should overwrite previous values.

**中文：**
實作一個 `StockPrice` 類別，支援在特定時間點更新股票價格，並查詢目前價格、最高價格及最低價格。同一時間點的更新應覆蓋舊值。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Overwrite existing timestamps? / 會覆蓋現有時間點嗎？ | Yes. / 會。 |
| Current price definition? / 目前價格的定義？ | Price at the maximum timestamp seen. / 已觀測到的最大時間點對應的價格。 |
| Efficiency requirement? / 效率要求？ | Avoid $O(N)$ scans for queries. / 查詢時應避免 $O(N)$ 掃描。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Source of Truth** | Use a `timestamp_to_price` Hash Map to always store the latest, correct price for any given time. / 使用 `timestamp_to_price` 哈希表儲存任何給定時間的最正確價格。 |
| **Lazy Heap Removal** | Maintain `min_heap` and `max_heap` for extrema. When querying, check if the heap's top matches the Hash Map. If not, pop and continue. / 使用最小堆與最大堆追蹤極值。查詢時，檢查堆頂元素是否與哈希表同步。若不同步，彈出並繼續。 |
| **Current Tracking** | Keep track of `max_timestamp` and its value during `update`. / 在 `update` 過程中追蹤 `max_timestamp` 及其對應數值。 |

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
import heapq

class StockPrice:
    def __init__(self):
        self.timestamp_price = {}
        self.latest_timestamp = -1
        self.min_heap = [] # (price, timestamp)
        self.max_heap = [] # (-price, timestamp)

    def update(self, timestamp: int, price: int) -> None:
        # Update current price tracking
        if timestamp >= self.latest_timestamp:
            self.latest_timestamp = timestamp
        
        # Update source of truth
        self.timestamp_price[timestamp] = price
        
        # Push to heaps (Lazy strategy)
        heapq.heappush(self.min_heap, (price, timestamp))
        heapq.heappush(self.max_heap, (-price, timestamp))

    def current(self) -> int:
        return self.timestamp_price[self.latest_timestamp]

    def maximum(self) -> int:
        # Lazy removal: pop until top matches Hash Map
        while -self.max_heap[0][0] != self.timestamp_price[self.max_heap[0][1]]:
            heapq.heappop(self.max_heap)
        return -self.max_heap[0][0]

    def minimum(self) -> int:
        # Lazy removal: pop until top matches Hash Map
        while self.min_heap[0][0] != self.timestamp_price[self.min_heap[0][1]]:
            heapq.heappop(self.min_heap)
        return self.min_heap[0][0]
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Update** | **O(log N)** | Pushing into two heaps. / 兩次堆疊 Push 操作。 |
| **Current** | **O(1)** | Direct Hash Map lookup. / 哈希表直接查找。 |
| **Max/Min** | **O(log N) Amortized** | Each entry pushed once is popped at most once across all queries. / 每個記錄最多被彈出一次。 |
| **Space** | **O(N)** | Storing timestamps in Hash Map and Heaps. / 哈希表與堆疊儲存所有資料。 |

---

## 6. Actionable Corrections (改進行動)

**English:**
1. **Handle Empty Initialization:** Remember to define initial states (like `-1` or `None`) to prevent crashes before the first update.
2. **Lazy Removal vs TreeMap:** In Java/C++, a `TreeMap` (SortedMap) could provide $O(\log N)$ for all. In Python, the Heap + Lazy Removal is the standard "Google-tier" alternative.

**中文：**
1. **處理空狀態：** 記得定義初始狀態（如 `-1` 或 `None`），避免在第一次更新前呼叫查詢時崩潰。
2. **延遲刪除 vs TreeMap：** 在 Java/C++ 中可用 `TreeMap` 解決。在 Python 中，堆疊 + 延遲刪除是標準的「Google 等級」替代方案。

---

## 7. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Source of Truth** | The single point where information is guaranteed to be correct | 唯一事實來源 |
| **Lazy Removal** | Deleting stale data only when it reaches the top of a priority structure | 延遲刪除 |
| **Amortized Analysis** | The average time per operation over a sequence of operations | 攤銷分析 |
| **Min-Heap / Max-Heap** | Data structures that provide O(1) access to min/max elements | 最小堆 / 最大堆 |
| **OOD** | Object-Oriented Design focusing on class structure and state | 物件導向設計 |
