# Coding Interview: Connected Components in a Doubly Linked List (雙向鏈結串列的連通分量)

**Topic / 主題:** Linked List & Hash Set / 鏈結串列與哈希集合
**Difficulty / 難度:** Medium
**Target Level / 目標等級:** Google L4
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-11

---

## 1. Problem Statement (題目)

**English:**
Given a list of `Node` objects from one or more doubly linked lists (provided in random order), find the number of connected components. A connected component is a maximal group of nodes that are directly linked in the original structure.

**中文：**
給定一組來自一個或多個雙向鏈結串列的 `Node` 物件（以隨機順序提供），請找出連通分量的數量。連通分量是指在原始結構中直接相連的一組節點的最大集合。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Null pointers at head/tail? / 頭尾指標是否為空？ | Yes, `node.prev` is `None` for heads, `node.next` is `None` for tails. / 是的。 |
| Cycles in the list? / 原始串列是否有環？ | No, assume linear structures. / 沒有，假設為線性結構。 |
| Order of input? / 輸入順序？ | Random. / 隨機。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Boundary Counting** | A connected component can be uniquely identified by its "head". A node is a head of a component if its `prev` node is either `None` or not present in the input set. / 一個連通分量可以由其「頭部」唯一標識。如果一個節點的 `prev` 為空，或者其 `prev` 不在輸入集合中，該節點就是一個分量的頭部。 |
| **Hash Set Lookup** | Convert the input list into a `set` for $O(1)$ presence checks. / 將輸入清單轉換為 `set` 以實現 $O(1)$ 的存在檢查。 |
| **Single Pass** | Iterate through the input list exactly once, incrementing the count whenever a "head" node is encountered. / 遍歷輸入清單一次，每當遇到「頭部」節點時增加計數。 |

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
from typing import List

class Solution:
    def countComponents(self, input_nodes: List['Node']) -> int:
        if not input_nodes:
            return 0
            
        # O(N) space for O(1) lookups
        node_set = set(input_nodes)
        count = 0
        
        for node in input_nodes:
            # Condition for a node to be the START of a component:
            # 1. It is the absolute head of the original list (prev is None)
            # OR
            # 2. Its previous neighbor was NOT picked in our input set
            if node.prev is None or node.prev not in node_set:
                count += 1
                
        return count
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Time / 時間** | **O(N)** | Converting to set takes O(N), and the single pass takes O(N). / 轉換為集合與單次遍歷均為線性時間。 |
| **Space / 空間** | **O(N)** | Storing the input nodes in a Hash Set for fast lookup. / 在哈希集合中儲存輸入節點。 |

---

## 6. Actionable Corrections (改進行動)

**English:**
1. **From Traversal to Logic:** The candidate initially thought of a "traverse and remove" approach. Moving to "boundary counting" is a significant optimization that simplifies the code and reduces constant factor overhead.
2. **Object Identity:** In Python, `set(input_nodes)` uses the identity/hash of the objects. This is correct as we are given actual `Node` objects, not just values.

**中文：**
1. **從遍歷轉向邏輯判斷：** 候選人最初考慮的是「遍歷並刪除」法。轉向「邊界計數法」是一個顯著的優化，簡化了代碼並減少了常數項開銷。
2. **物件一致性：** 在 Python 中，`set(input_nodes)` 使用物件的雜湊值。由於題目給的是 `Node` 物件而非單純數值，這種做法是正確的。

---

## 7. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Connected Component** | A subset of nodes where any two nodes are connected by paths | 連通分量 |
| **Doubly Linked List** | A list where each node has pointers to both next and previous nodes | 雙向鏈結串列 |
| **Boundary Condition** | A condition used to identify the start or end of a sequence | 邊界條件 |
| **Set Membership** | Checking if an element exists within a collection | 集合成員檢查 |
| **Identity Lookup** | Searching based on memory address/object hash rather than value | 物件標識查找 |
