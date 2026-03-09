# Linked List (鏈結串列)

### 📌 核心概念
由節點（Node）組成，每個節點包含資料與指向下個節點的指標。記憶體不連續。

### 📌 適用情境 (何時該想到它？)
- 題目明確給定 Linked List。
- 頻繁在中間進行插入與刪除操作。
- 實作 LRU Cache 或 LFU Cache。

### 📌 優缺點分析 (Trade-offs)
- **優點**：插入與刪除只要 O(1)（若已知節點位置），不需要預先分配記憶體。
- **缺點**：無法 O(1) 隨機存取（必須從頭遍歷 O(N)）；對 Cache 不友善。

### 📌 實作技巧
- **Dummy Node（哨兵節點）**：永遠建立一個 Dummy 節點指向 Head，可以免去處理 Head 為 Null 或 Head 需要變動的大量 Edge Cases。
- **快慢指針**：用來找中點或是判斷是否有環。

### 💻 經典模板與 Sample Code

#### 模板：反轉鏈結串列 (O(1) 空間)
必須熟練到能默寫。關鍵在於利用三個指標 `prev`, `curr`, `next_node` 來打斷並重新連接。
**Python**:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head: ListNode) -> ListNode:
    prev = None
    curr = head
    while curr:
        next_node = curr.next  # 1. 暫存下一個節點
        curr.next = prev       # 2. 反轉當前節點指標
        prev = curr            # 3. prev 前進
        curr = next_node       # 4. curr 前進
    return prev # 回傳新的 Head
```

#### 模板：Dummy Node 與 快慢指針找中點
**Python**:
```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def findMiddle(head: ListNode) -> ListNode:
    slow = fast = head
    # 當 fast 能跳兩步時才繼續
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow # slow 此時就在中點
```
