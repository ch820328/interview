# Heaps & Priority Queues: Expert Guide (堆疊與優先級隊列：專家級指南)

## I. Problem Statement & Nuances (題目與細節)
How do you efficiently manage a collection of items where you constantly need to access the minimum or maximum? Why are Heaps preferred over Sorted Arrays for dynamic priority management?
如何在需要頻繁存取最小值或最大值的情況下，有效率地管理資料集合？為什麼在動態優先級管理中，堆疊 (Heap) 優於排序後的陣列 (Sorted Array)？

**Nucleus Insights (核心觀點):**
- **Dynamic Re-ordering**: Heaps don't keep the *entire* collection sorted; they only maintain the **Heap Property**. (堆疊不保持「全體」排序，僅維持「堆疊屬性」，這大幅平衡了讀寫成本。)
- **Array-Based Representation**: A Binary Heap is conceptually a tree but physically stored as an **Array** to maximize cache locality. (二元堆疊在概念上是樹，但在物理上存儲為陣列，以最大化快取局部性。)
- **Stability**: Heaps are generally not stable; the relative order of equal elements is not guaranteed. (堆疊通常是不穩定的；相同元素的相對順序不獲保證。)

---

## II. Mechanical Deep-Dive: Heapify & Rebalancing (底層原理：Heapify 與平衡)

A Binary Heap is a **Complete Binary Tree**.
二元堆疊是一個**完全二元樹**。

1. **Mapping to Array (映射至陣列)**:
   - Parent of index $i$: `(i - 1) / 2`
   - Left child of index $i$: `2*i + 1`
   - Right child of index $i$: `2*i + 2`
2. **Sift-Up (Percolate Up)**: Moving an element up to restore heap order after an insertion ($O(\log N)$). (插入後將元素上移以恢復順序。)
3. **Sift-Down (Percolate Down)**: Moving an element down after removing the root ($O(\log N)$). (移除根節點後將元素下移。)

---

## III. Quantitative Analysis Table (量化指標分析)

| Operation (操作) | Heap (堆疊) | Sorted Array (排序陣列) | Hash Map (哈希表) |
|---|---|---|---|
| **Find Min/Max** | $O(1)$ | $O(1)$ | $O(N)$ (Search) |
| **Insert** | $O(\log N)$ | $O(N)$ (Shift) | $O(1)$ (Avg) |
| **Delete Min/Max** | $O(\log N)$ | $O(N)$ | $O(N)$ |
| **Build Heap** | **$O(N)$** | $O(N \log N)$ (Sort) | $O(N)$ |

*Expert Note: Building a heap takes $O(N)$, not $O(N \log N)$, because the number of elements at lower levels (where work is minimal) is greater.*

---

## IV. Infrastructure Ecosystem (基礎設施生態系)

| Tool/Library | Use Case (使用場景) |
|---|---|
| **OS Scheduler** | Managing process tasks based on priority (CFS). (根據優先級管理行程任務。) |
| **Dijkstra’s Algo** | Finding the next closest vertex in $O(\log V)$. (在 $O(\log V)$ 內尋找下一個最近頂點。) |
| **Data Streaming** | Finding the "Top K" elements in a real-time stream. (在即時流中尋找「Top K」元素。) |
| **Load Balancing** | Least-connection scheduling. (最小連接數調度。) |

---

## V. Code: Production Grade (Min-Heap in Go / Go 語言最小堆疊)

```go
package main

import (
    "container/heap"
    "fmt"
)

// An Item is something we manage in a priority queue.
type Item struct {
    value    string // The value of the item
    priority int    // The priority (e.g., latency, cost)
    index    int    // Internal index managed by 'heap'
}

type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }
func (pq PriorityQueue) Less(i, j int) bool { return pq[i].priority < pq[j].priority }
func (pq PriorityQueue) Swap(i, j int) {
    pq[i], pq[j] = pq[j], pq[i]
    pq[i].index, pq[j].index = i, j
}

func (pq *PriorityQueue) Push(x interface{}) {
    n := len(*pq)
    item := x.(*Item)
    item.index = n
    *pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() interface{} {
    old := *pq
    n := len(old)
    item := old[n-1]
    item.index = -1 // for safety
    *pq = old[0 : n-1]
    return item
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Priority Tying**: If many items have the same priority, the order of extraction depends on the implementation. This can lead to **unfairness** if not handled. (若多個項目優先級相同，提取順序取決於實現，可能導致「不公平」。)
2. **Dynamic Update**: Updating the priority of an existing element in a heap requires $O(\log N)$ and an auxiliary map to find the index quickly. (更新既有元素的優先級需要 $O(\log N)$，通常需要一個輔助哈希表來快速搜尋索引。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Binary Heap | 二元堆疊 | A complete binary tree used to implement priority queues. (用於實現優先級隊列的完全二元樹。) |
| Max-Heap | 最大堆疊 | Heap where parents are always greater than or equal to children. (父節點始終大於或等於子節點的堆疊。) |
| Priority Inversion | 優先級倒置 | Scenario where low priority tasks delay high priority ones. (低優先級任務延誤高優先級任務的情境。) |
| K-way Merge | K 路歸併 | Using a heap to merge multiple sorted streams efficiently. (利用堆疊有效地合併多個排序後的流。) |
