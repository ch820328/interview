# Syllabus: Insert Delete GetRandom O(1)

## 1. Problem Statement & Constraints / 題目描述與約束
**English:**  
Implement the `RandomizedSet` class:
- `insert(val)`: Inserts an item `val` into the set if not present. Returns `true` if the item was not present, `false` otherwise.
- `remove(val)`: Removes an item `val` from the set if present. Returns `true` if the item was present, `false` otherwise.
- `getRandom()`: Returns a random element from the current set of elements. Each element must have the same probability of being returned.
Average $O(1)$ time complexity is required for all functions.

**Chinese (Traditional):**  
實作 `RandomizedSet` 類別：
- `insert(val)`：若 `val` 不在集合中則插入。若成功插入傳回 `true`，否則傳回 `false`。
- `remove(val)`：若 `val` 在集合中則移除。若成功移除傳回 `true`，否則傳回 `false`。
- `getRandom()`：從目前集合中隨機取得一個元素。每個元素被取得的機率必須相同。
所有函數的平均時間複雜度皆須為 $O(1)$。

## 2. Clarification Q&A / 澄清與問答
| Question (EN) | Answer (EN) | Question (ZH) | Answer (ZH) |
|---|---|---|---|
| Can we use built-in random? | Yes, `random.choice` is acceptable. | 可以使用內建隨機函數嗎？ | 可以，`random.choice` 是可接受的。 |
| Handle duplicates? | No, it's a "Set", so duplicates return `false` on insert. | 需要處理重複值嗎？ | 不需要，這是「集合」，插入重複值應傳回 `false`。 |

## 3. Brute Force vs Optimal / 暴力法 vs 最優解
| Method | Time Complexity (`insert`/`remove`/`rand`) | Space | Notes |
|---|---|---|---|
| **Hash Set Only** | $O(1)$ / $O(1)$ / **$O(N)$** | $O(N)$ | Native sets don't support index-based random access in $O(1)$. |
| **List Only** | $O(1)$ / **$O(N)$** / $O(1)$ | $O(N)$ | Removal in a list takes linear time to find and shift. |
| **Hash Map + List (Optimal)** | **$O(1)$ / $O(1)$ / $O(1)$** | $O(N)$ | Map stores value -> index. List stores values. Use swap-with-last to remove in $O(1)$. |

## 4. Final Solution (Python) / 最終代碼
```python
import random

class RandomizedSet:
    def __init__(self):
        self.nums = []
        self.val_to_idx = {}

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False
        self.val_to_idx[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False
        idx_to_remove = self.val_to_idx[val]
        last_val = self.nums[-1]
        
        # Swap with last element
        self.nums[idx_to_remove] = last_val
        self.val_to_idx[last_val] = idx_to_remove
        
        # Pop last
        self.nums.pop()
        del self.val_to_idx[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.nums)
```

## 5. Dry Run Sequence / 逐步執行追蹤
**Sequence:** `insert(1)`, `insert(2)`, `remove(1)`
| Step | Op | Map State | List State | Note |
|---|---|---|---|---|
| 1 | `ins(1)` | `{1: 0}` | `[1]` | Append to end. |
| 2 | `ins(2)` | `{1: 0, 2: 1}` | `[1, 2]` | Append to end. |
| 3 | `rem(1)` | `{2: 0}` | `[2]` | Move `2` to index `0`, update map, then pop. |

## 6. Common Bugs / 常見錯誤
| Bug | Prevention (預防方式) |
|---|---|
| Wrong index after swap | Update the map for the **last element** before popping. (在 pop 之前，務必先更新「原本最後一個元素」在 Map 中的索引) |
| $O(N)$ Removal | Ensure you use the swap-to-last technique instead of direct `list.remove()`. (確保使用交換至末端的技巧，而非直接呼叫 `list.remove()`) |

## 7. Full Evaluation / 完整評估 (Bilingual)
**Rating: Strong Hire / 強烈建議錄取評等**

**Strengths (優點):**
- Mastered the List + Hash Map combination for $O(1)$ constraints. (熟練掌握 List + Hash Map 組合以達成 $O(1)$ 約束。)
- Correctly identified the swap-to-last optimization for removal. (正確識別出交換至末端以進行 $O(1)$ 刪除的優化技巧。)

**Actionable Corrections (可執行的改進建議):**
- Be cautious about non-uniform random implementations; always use standard libraries like `random.choice`. (留意非均勻的隨機實作；應一律使用 `random.choice` 等標準函式庫。)

---

## 8. Technical Term Dictionary (Appendix) / 技術名詞字典 (附錄)

**English:**
- **Dynamic Array (List):** A random-access data structure that allows adding/removing elements. In Python, `list` is a dynamic array.
- **Hash Map (Dict):** A structure that maps keys to values using a hash function, providing $O(1)$ average time for operations.
- **Amortized Time Complexity:** The average time per operation over a sequence of operations (e.g., list append is usually $O(1)$ but occasionally $O(N)$ when resizing).
- **Uniform Distribution:** A type of probability distribution in which all outcomes are equally likely.
- **In-place Swap:** Swapping elements within a data structure without using additional memory proportional to the size of the structure.

**Chinese (Traditional):**
- **動態陣列 (Dynamic Array)：** 一種支援隨機存取的資料結構。在 Python 中，`list` 即為動態陣列。
- **雜湊表 (Hash Map)：** 使用雜湊函數將鍵映射到值的結構，提供平均 $O(1)$ 的操作時間。
- **均攤時間複雜度 (Amortized Time Complexity)：** 一系列操作中，單次操作的平均時間（例如 list append 通常是 $O(1)$，但擴容時為 $O(N)$）。
- **均勻分佈 (Uniform Distribution)：** 一種所有結果發生機率皆相等的機率分佈。
- **原地交換 (In-place Swap)：** 在資料結構內部交換元素，而不使用與結構大小成比例的額外記憶體。
