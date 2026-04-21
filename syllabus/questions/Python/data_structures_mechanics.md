# Python Data Structures: Internal Mechanics (Python 資料結構：底層機制解析)

## I. Problem Statement & Nuances (題目與細節)
What are the internal differences between Lists and Tuples? How does Python implement its Dictionary for $O(1)$ performance? Explain the memory overheads involved.
Python 的列表 (List) 與元組 (Tuple) 的底層差異為何？Python 如何實現字典 (Dictionary) 以達到 $O(1)$ 的效能？請解釋相關的記憶體開銷。

**Nucleus Insights (核心觀點):**
- **Over-allocation Strategy**: Python Lists use a dynamic dynamic array strategy, allocating more space than needed to ensure $O(1)$ amortized insertion. (Python 列表使用動態陣列策略，預分配額外空間以確保攤還 $O(1)$ 插入。)
- **Immutability & Slot Reuse (Tuple)**: Tuples are immutable, allowing Python to optimize memory by pre-calculating hash and reusing handles. (元組不可變，允許 Python 透過預計算與控制代碼重用來優化記憶體。)
- **Hash Table Evolution (Dict)**: Modern Python (3.6+) dictionaries maintain **insertion order** while using highly optimized hash collision strategies. (現代 Python 字典在保持插入順序的同時，使用了高度優化的高效哈希碰撞策略。)

---

## II. Mechanical Deep-Dive: List vs. Tuple (底層原理：列表與元組)

### 1. Python List (動態陣列)
- **Structure**: A pointer array to `PyObject`.
- **Memory Allocation**: Uses a **4, 8, 16, 25, 35...** growth pattern to minimize `realloc` calls. (使用階梯式增長模式以減少重新分配次數。)
- **Detail**: When a list is deleted, Python keeps its internal array around (Free List) for a while to reuse it for the next list. (刪除後會暫時保留基礎空間以利重用。)

### 2. Python Tuple (不可變元組)
- **Structure**: Fixed-size `PyObject` array.
- **Optimization**: "Interning" for small empty tuples. Because they are immutable, they can be safely shared across the program. (小型空元組的「實習」與共享機制。)

---

## III. Quantitative Analysis Table (量化指標分析)

| Feature (特性) | List (列表) | Tuple (元組) | Golang Slice (對比) |
|---|---|---|---|
| **Storage** | Dynamic / Mutable | Fixed / Immutable | Dynamic / Pointer to Array |
| **Lookup** | $O(1)$ | $O(1)$ | $O(1)$ |
| **Overhead** | High (Internal overhead) | Low (Fixed size) | Medium (Header: 24 bytes) |
| **Insertion** | Amortized $O(1)$ | N/A (Requires new tuple) | Amortized $O(1)$ |

---

## IV. Dictionary: The Open Addressing Hash Map

Python Dicts use **Open Addressing** with a special collision resolution algorithm (Perturbation).
Python 字典使用**開放定址法**配合特殊的碰撞解決演算法。

- **Compact Layout (3.6+)**: Python now uses two arrays for Dicts: an `indices` array and an `entries` array. This makes them **ordered** and reduces memory by ~20%. (使用索引陣列與條目陣列分離，既保證順序又節省空間。)
- **Load Factor**: Resizes when the table is 2/3 full. (容量達到 2/3 時會自動擴容。)

---

## V. Code: Memory Footprint Trace (記憶體佔用追蹤)

```python
import sys

# Expert: Compare memory of List vs Tuple
# 專家級：對比列表與元組的記憶體足跡
l = [1, 2, 3]
t = (1, 2, 3)

print(f"List size: {sys.getsizeof(l)} bytes")   # Output: ~88 bytes
print(f"Tuple size: {sys.getsizeof(t)} bytes")  # Output: ~64 bytes

# Proving over-allocation in List
l2 = []
for i in range(5):
    l2.append(i)
    # The size jumps at specific intervals (快取在特定間隔跳躍)
    print(f"Items: {len(l2)}, Bytes: {sys.getsizeof(l2)}")
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Large List In-place Deletion**: Removing elements from the *middle* of a large list is $O(N)$ because all subsequent pointers must be shifted. **Solution**: Use `collections.deque` for $O(1)$ pop/push from ends. (從中間刪除元素會導致 $O(N)$ 移動開銷。)
2. **Dict Collision Attack**: If keys have identical hashes, performance drops to $O(N)$. Python uses per-process hash randomization to mitigate this. (哈希碰撞攻擊會讓效能降至 $O(N)$。)
3. **Implicit Copies**: Adding two lists `a + b` creates a whole new list, consuming $O(N+M)$ memory. (列表相加會產生全新的副本，大幅增加記憶體消耗。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Amortized Constant Time| 攤還常數時間 | Average time taken per operation over many operations. (多次操作下的平均固定耗時。) |
| Open Addressing | 開放定址法 | Collision resolution where new slots are searched linearly or pseudo-randomly. (在哈希表中使用搜尋空槽解決碰撞。) |
| PyObject_HEAD | Python 對象頭部 | The macro defining standard header for Python objects (refcount, type). (定義 Python 對象標準頭部的宏。) |
| List Comprehension | 列表推導式 | Optimized syntax for creating lists from other iterables. (從其他可迭代對象創建列表的優化語法。) |
