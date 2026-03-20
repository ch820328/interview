# Syllabus: LRU Cache (Design / Linked List + Hash Map)

## 1. Problem Statement & Constraints / 題目描述與約束
**English:**  
Design a data structure that follows the constraints of a Least Recently Used (LRU) cache. Implement the `LRUCache` class with `get(key)` and `put(key, value)`. Both operations must run in $O(1)$ average time complexity.

**Chinese (Traditional):**  
設計一個遵循最近最少使用 (LRU) 快取約束的資料結構。實作 `LRUCache` 類別，包含 `get(key)` 與 `put(key, value)` 方法。這兩個操作的平均時間複雜度都必須為 $O(1)$。

**Constraints:**
- $1 \le \text{capacity} \le 3000$
- $0 \le \text{key}, \text{value} \le 10^5$
- At most $2 \times 10^5$ calls will be made to `get` and `put`.

## 2. Clarification Q&A / 澄清與問答
| Question (EN) | Answer (EN) | Question (ZH) | Answer (ZH) |
|---|---|---|---|
| Can capacity be 0? | No, constraints say capacity $\ge 1$. | 容量可以是 0 嗎？ | 不行，約束條件說明容量 $\ge 1$。 |
| Can keys/values be negative? | They are $0 \le k, v \le 10^5$, but the logic should handle any integer. | 鍵與值可以是負數嗎？ | 題目給定限制為正整數，但邏輯應能處理任何整數。 |

## 3. Brute Force vs Optimal / 暴力法 vs 最優解
| Method | Time Complexity (`get`/`put`) | Space Complexity | Notes |
|---|---|---|---|
| **Array / Simple List** | $O(N)$ / $O(N)$ | $O(C)$ | Searching for a key or shifting elements to maintain order takes linear time. |
| **Optimal (Hash Map + DLL)** | $O(1)$ / $O(1)$ | $O(C)$ | Hash Map provides $O(1)$ lookup to the exact node. Doubly Linked List provides $O(1)$ removal and insertion at the head. |

## 4. Final Solution (Python) / 最終代碼
```python
class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Helper to remove a node from the linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node: Node):
        """Helper to insert a node right after the dummy head."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.val

    def put(self, key: int, val: int):
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
            
            new_node = Node(key, val)
            self._add_to_head(new_node)
            self.cache[key] = new_node
```

## 5. Dry Run Sequence / 逐步執行追蹤
**Operations:** `LRUCache(2)`, `put(1,1)`, `put(2,2)`, `get(1)`, `put(3,3)`

| Step | Operation | Cache Dict State | DLL State (Head to Tail) |
|---|---|---|---|
| 1 | `put(1,1)` | `{1: Node(1)}` | `H <-> [1,1] <-> T` |
| 2 | `put(2,2)` | `{1: Node(1), 2: Node(2)}` | `H <-> [2,2] <-> [1,1] <-> T` |
| 3 | `get(1)` | `{1: Node(1), 2: Node(2)}` | `H <-> [1,1] <-> [2,2] <-> T` |
| 4 | `put(3,3)` | `{1: Node(1), 3: Node(3)}` | `H <-> [3,3] <-> [1,1] <-> T` (Node 2 evicted) |

## 6. Common Bugs / 常見錯誤
| Bug | Prevention (預防方式) |
|---|---|
| `AttributeError: NoneType has no attribute 'prev'` <br> (邊界處理錯誤) | Use **Dummy Head** and **Dummy Tail** nodes. This guarantees every inserted node always has a valid `prev` and `next`. (使用虛擬頭尾節點，保證拔插時不會出現 None) |
| Forgetting to delete from Map <br> (忘記從 Hash Map 中刪除) | When evicting from the tail, you must also `del self.cache[lru_node.key]`. This is why the `Node` must store the `key` as well as the `val`. (從鏈表尾端移除節點時，也必須從字典中刪除鍵，這也是為什麼 Node 中必須同時存儲 Key 的原因) |

## 7. Full Evaluation / 完整評估 (Bilingual)
**Rating: Strong Hire / 強烈建議錄取評等**

**Strengths (優點):**
- Candidate correctly opted for Dummy Nodes to bypass all edge-case `if` logic. (面試者正確地選擇了虛擬節點，避開了所有邊界條件的 if 判斷。)
- Extracted pointer manipulation into `_remove` and `_add_to_head` helpers, resulting in highly readable core functions. (將指針操作抽離成輔助函數，使得核心方法極具可讀性。)

**Gaps to L4+ (需改進處):**
- Avoid minor syntax/typo issues if coding on a whiteboard. (在白板面試時需注意避免變數名稱錯字等小問題。)
