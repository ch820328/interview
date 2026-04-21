# Python Dictionary: Internal Deep-Dive (Python 字典：源碼級深度解析)

## I. Evolution: From Hash Table to Compact Dict (演進過程)
Before Python 3.6, dictionaries were large, sparse hash tables with poor memory locality. PEP 468 introduced the **Compact Dict**.
在 Python 3.6 之前，字典是巨大的稀疏哈希表；PEP 468 引入了「緊湊型字典」。

### 1. Old Layout (Pre-3.6)
Every row in the table was a `PyDictEntry` ($24$ bytes) containing `hash`, `key`, and `value`. This resulted in a lot of empty space.
每一行都是一個 24 字節的條目，包含哈希值、鍵與值，導致大量空間浪費。

### 2. New Compact Layout (3.6+)
Dictionaries now use two separate arrays:
1. **Indices Array** (`dk_indices`): A sparse array of small integers (1 or 2 bytes each). (稀疏的索引陣列。)
2. **Entries Array** (`dk_entries`): A dense array of `PyDictKeyEntry` where items are stored in **insertion order**. (緊湊的條目陣列，按插入順序排序。)

---

## II. The Perturbation Algorithm (碰撞解決演算法)

Python doesn't use simple linear probing ($i = i+1$) because it causes clustering. It uses a **Perturbation Logic** to jump across the table.
Python 不使用簡單的線性探測，而是使用一種基於位元運算的「擾動邏輯」來解決碰撞。

**The Formula (核心公式):**
$$j = (5 \times j + 1 + \text{perturb}) \pmod{2^n}$$
- `perturb` is initialized to the `hash`.
- In each step, `perturb >>= 5`.
- This ensures that all bits of the hash eventually influence the probing sequence. (確保哈希值的所有位元都能影響探測順序。)

---

## III. Quantitative Analysis: Memory Savings (量化指標)

Assume a dictionary with 1,000 entries (requiring a table size of 2,048):
假設一個有 1,000 個條目的字典（哈希表大小需為 2,048）：

| Feature | Old Dict (Pre-3.6) | New Compact Dict (3.6+) |
|---|---|---|
| **Entry Storage** | $2048 \times 24 = 49,152$ bytes | $1000 \times 24 = 24,000$ bytes |
| **Index Overhead** | $0$ | $2048 \times 1 = 2,048$ bytes |
| **Total Memory** | **~49 KB** | **~26 KB (Saved ~47%)** |
| **Iteration** | Scanning sparse table. | Scanning dense `entries`. (**Faster!**) |

---

## IV. Professional Nuances: Hash Collision Attack (專業細節)

**Q:** If multiple keys generate the same hash, what happens?
1. **Performance Degrades**: Lookup becomes $O(N)$.
2. **Security Risk**: Attackers can flood a server with colliding keys (SipHash mitigation).
3. **Randomization**: Python uses a random "Salt" for each process start to randomize hashes. (每個進程啟動時會有隨機鹽值。)

---

## V. C-Source Reference (C 語言源碼參考)

```c
// Objects/dictobject.c
typedef struct {
    Py_hash_t me_hash;
    PyObject *me_key;
    PyObject *me_value;
} PyDictKeyEntry;
```
*Expert Note: The `me_value` pointer is what makes Python dictionaries "Objects by reference". Only the address is stored.*

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Massive Deletions**: Deleting keys does not immediately shrink the `dk_indices`. The slots are marked as **Dummy** to ensure the probing sequence doesn't break. (刪除鍵不會立即縮小陣列，而是標記為 Dummy 以維持探測順序。)
2. **Re-hashing**: When the table is 2/3 full, it triggers a resize. This is an $O(N)$ operation that can cause a latency spike. (容量達 2/3 時會觸發擴容，導致瞬時延遲。)
3. **Custom `__hash__`**: If a custom object has a poor `__hash__` implementation, it can ruin dictionary performance. (自定義哈希實作不良會毀掉字典效能。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Open Addressing | 開放定址法 | Collision resolution strategy (Search for next empty slot). (搜尋下一個空槽的碰撞解決策略。) |
| Insertion Order | 插入順序 | The order in which keys were added to the dict. (鍵被加入字典的順序。) |
| Load Factor | 負載因子 | Ratio of used slots to total slots (2/3 in Python). (已使用槽與總槽數的比例。) |
| Dummy Slot | 虛擬槽 | A placeholder for a deleted key to preserve probing continuity. (為了保持探測連續性而保留的刪除位。) |
