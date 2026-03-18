# Employee Free Time (員工空閒時間)

## Problem Statement & Constraints (問題描述與限制條件)

**Problem Statement (問題描述):**
We are given a list `schedule` of employees, which represents the working time for each employee. Each employee has a list of non-overlapping Intervals, and these intervals are in sorted order. Return the list of finite intervals representing common, positive-length free time for all employees, also in sorted order.
給定一份員工的 `schedule`（排班表），代表每位員工的工作時間。每位員工有一組互不重疊且已排序的區間（Intervals）。請回傳所有員工共同的、正長度的空閒時間區間，且需按照排序回傳。

**Constraints (限制條件):**
- Each employee has at least one interval. (每位員工至少有一個區間。)
- Intervals are sorted by start time. (區間已按開始時間排序。)
- `0 <= start < end <= 10^8`. (區間範圍介於 0 到 10^8。)
- `k` (number of employees) and `N` (total intervals) are up to several thousands. (`k` 員工數與 `N` 總區間數可達數千。)

---

## Clarification Q&A (問答紀錄)

| Question (問題) | Answer (回答) |
|---|---|
| Are boundaries inclusive? `[4, 10]` mean busy at 4? (邊界包含嗎？`[4, 10]` 代表 4 號是忙碌的嗎？) | Yes, `[4, 10]` means the employee is strictly busy from 4 to 10 inclusive. (是的，`[4, 10]` 代表員工在 4 到 10 之間是忙碌的。) |
| What if the output is null? (如果沒有空閒時間怎麼辦？) | Return an empty list `[]`. (回傳空陣列 `[]`。) |
| Is there a time limit? (有時間範圍限制嗎？) | No specific 0-24 bound; time values can go up to `10^8`. (沒有 0-24 的限制；時間數值可達 `10^8`。) |

---

## Comparison Table: Brute Force vs Optimal (對比表：暴力法與最優解)

| Approach (方法) | Time Complexity (時間複雜度) | Space Complexity (空間複雜度) | Reasoning (推導) |
|---|---|---|---|
| **Brute Force (暴力掃描)** | $O(M)$ | $O(M)$ | Iterating through every unit of time up to $10^8$. (遍歷 $10^8$ 以內的每個時間單位。) |
| **Optimal: Heap (最優解：堆積)** | $O(N \log k)$ | $O(k)$ | Efficiently merge $k$ sorted lists using a Min-Heap. (使用最小堆積高效合併 $k$ 個排序清單。) |

---

## Python Code Solution (Python 程式解法)

```python
import heapq
from typing import List

class Interval:
    def __init__(self, start: int = 0, end: int = 0):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"[{self.start}, {self.end}]"

class Solution:
    def employeeFreeTime(self, schedule: List[List[Interval]]) -> List[Interval]:
        """
        Use a Min-Heap to perform a k-way merge of sorted employee schedules.
        Target Complexity: O(N log k) Time, O(k) Space.
        """
        pq = []
        # Initialize the heap with the first interval of each employee
        # 將每位員工的第一個區間放入堆積
        for i, emp_intervals in enumerate(schedule):
            if emp_intervals:
                heapq.heappush(pq, (emp_intervals[0].start, i, 0))
        
        res = []
        if not pq:
            return []
        
        # Pop the very first starting interval to establish the baseline end time
        # 取出第一個最開始的區間，建立基準結束時間
        first_start, emp_idx, int_idx = heapq.heappop(pq)
        prev_end = schedule[emp_idx][int_idx].end
        
        # Push the next interval for that employee
        # 推入該員工的下一個區間
        if int_idx + 1 < len(schedule[emp_idx]):
            next_int = schedule[emp_idx][int_idx + 1]
            heapq.heappush(pq, (next_int.start, emp_idx, int_idx + 1))

        while pq:
            curr_start, emp_idx, int_idx = heapq.heappop(pq)
            
            # If current start is greater than the running end, we found a gap
            # 如果當前開始時間大於累計結束時間，代表找到空隙
            if curr_start > prev_end:
                res.append(Interval(prev_end, curr_start))
            
            # Update the running end time to the furthest completion
            # 更新累計結束時間為目前最遠的完成點
            prev_end = max(prev_end, schedule[emp_idx][int_idx].end)
            
            # Continue the k-way merge
            # 繼續完成 $k$ 路合併
            if int_idx + 1 < len(schedule[emp_idx]):
                next_int = schedule[emp_idx][int_idx + 1]
                heapq.heappush(pq, (next_int.start, emp_idx, int_idx + 1))
                
        return res
```

---

## Step-by-Step Dry Run (逐步執行表)

**Input (輸入):** `schedule = [[[1,2],[5,6]],[[1,3]],[[4,10]]]`

| Step (步驟) | Heap State (堆積狀態) | prev_end (累計終點) | Gap Found (發現空隙) |
|---|---|---|---|
| 1 | `[(1, 0, 0), (1, 1, 0), (4, 2, 0)]` | 2 | None |
| 2 | `[(1, 1, 0), (4, 2, 0), (5, 0, 1)]` | 3 | None (1 <= 2) |
| 3 | `[(4, 2, 0), (5, 0, 1)]` | 10 | **[3, 4]** (4 > 3) |
| 4 | `[(5, 0, 1)]` | 10 | None (5 <= 10) |

---

## Common Bugs (常見錯誤)

| Bug (錯誤) | Why it Happens (發生原因) | Fix (修正方法) |
|---|---|---|
| Missed overlapping gap (忽略重疊空隙) | Logic only checks the end of the *last popped* interval. (邏輯僅檢查上一個彈出區間的終點。) | Maintain a `prev_end` that is the `max` of all processed intervals. (維持一個 `prev_end` 作為所有已處理區間的最大值。) |
| Empty input error (空輸入錯誤) | Accessing `heapq.heappop(pq)` on an empty heap. (嘗試在空堆積上執行彈出。) | Add defensive `if not pq` checks. (增加防禦性的空值檢查。) |

---

## Final Evaluation (最終評估)

1. **Module Completed (完成模組):** Coding — Employee Free Time (Heap / K-way Merge)
2. **Overall Rating (整體評分):** **Strong Hire** (Grade strictly for L4 Bar)
3. **Strengths / Pros (優點):**
   - Correctly identified that $O(N \log k)$ beats sorting all $N$ intervals. (正確識別 $O(N \log k)$ 優於將所有 $N$ 個區間排序。)
   - Clean implementation using Python's `heapq`. (使用 Python 的 `heapq` 實作簡潔。)
   - Excellent awareness of edge case Handling (empty schedules). (優異的邊界條件處理意識。)
4. **Critical Gaps (關鍵差距):** None. (無。)
5. **Actionable Corrections (行動建議):** Continue practicing multi-list merge patterns as they are frequent in Google L4 interviews. (繼續練習多清單合併模式，這是 Google L4 面試的常見考點。)

---

## Technical Term Dictionary / Glossary (技術術語表)

| Term (術語) | English Definition | Chinese Translation (中文翻譯) |
|---|---|---|
| **Heap / Priority Queue** | A data structure that allows O(1) access to the min/max element. | **堆積 / 優先隊列**：一種允許以 O(1) 複雜度訪問最小/最大元素的數據結構。 |
| **K-way Merge** | Merging K sorted arrays into a single sorted array efficiently. | **K 路合併**：將 K 個排序好的數列高效合併為單一數列的過程。 |
| **Interval** | A continuous range defined by a start and end point. | **區間**：由起點與終點定義的一段連續範圍。 |
| **Greedy** | An algorithm design that makes the local optimal choice at each step. | **貪婪演算法**：在每一步都選擇局部最優解的演算法設計方式。 |
