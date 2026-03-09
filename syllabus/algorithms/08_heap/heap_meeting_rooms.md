# Google L4/L5 Coding Mock Interview — Meeting Rooms II
# Google L4/L5 程式編碼模擬面試 — 會議室 II

**Interviewer:** Google Coding Interviewer (L5 Standard)
**Topic / 主題:** Heap / Greedy | 堆積 / 貪婪演算法
**Rating / 評級:** Lean Hire

---

## 📝 Problem Statement | 題目

Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return the **minimum number of conference rooms** required to hold all meetings simultaneously.

給定一個會議時間區間陣列 `intervals`，其中 `intervals[i] = [start_i, end_i]`，回傳同時舉行所有會議所需的**最少會議室數量**。

```
Input:  [[0,30],[5,10],[15,20]]   → Output: 2
Input:  [[7,10],[2,4]]           → Output: 1
Input:  [[1,3],[3,5]]            → Output: 1  ← boundary case
```

**Constraints / 限制:**
- `1 <= intervals.length <= 10^4`
- `0 <= start_i < end_i <= 10^6`
- Intervals are **half-open**: `[start, end)` — if A ends at 3 and B starts at 3, only **1 room** needed.
- 區間為**半開區間**：A 在時間 3 結束，B 在時間 3 開始 → 只需 **1 間**會議室。
- Input is **read-only** — do not mutate `intervals`.
- 輸入為**唯讀**，不可修改 `intervals` 陣列。

---

## 🔍 Clarification Phase | 釐清階段

| Question | Answer |
|---|---|
| If A's end == B's start, 1 or 2 rooms? | **1 room** — treat as half-open interval `[start, end)` |
| Can I mutate the input (`.sort()`)? | **No** — treat input as read-only. Use `sorted()`. |

---

## 💡 Approach | 解題思路

### Brute Force | 暴力法
- Maintain a list tracking how many meetings are active at each time point.
- O(N²) time, O(N) space.

### Optimal: Min-Heap on End Times | 最優解：對結束時間使用最小堆積

**Core Insight / 核心思想:**
Sort by start time. Use a min-heap to always track the room that frees up earliest.
依開始時間排序，用最小堆積追蹤最早結束的房間。

**Algorithm / 演算法:**
1. Sort a **copy** of intervals by `start` time → O(N log N)
2. Push the first meeting's `end` time onto the heap.
3. For each subsequent meeting `[start, end]`:
   - If `start >= heap[0]` (earliest ending room): **reuse** it → `heapreplace(heap, end)`
   - Else: **new room needed** → `heappush(heap, end)`
4. Return `len(heap)` — the number of rooms in use.

**Complexity / 複雜度:**
- Time: **O(N log N)** — sort + N heap operations each O(log N)
- Space: **O(N)** — heap stores at most N end times

---

## ✅ Final Solution | 最終解答

```python
import heapq

class Solution:
    def minMeetingRooms(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0

        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        rooms_heap = []
        heapq.heappush(rooms_heap, sorted_intervals[0][1])

        for i in range(1, len(sorted_intervals)):
            start, end = sorted_intervals[i]
            if start >= rooms_heap[0]:
                heapq.heapreplace(rooms_heap, end)
            else:
                heapq.heappush(rooms_heap, end)

        return len(rooms_heap)

if __name__ == "__main__":
    solver = Solution()
    print(solver.minMeetingRooms([[0, 30], [5, 10], [15, 20]]))  # 2
    print(solver.minMeetingRooms([[7, 10], [2, 4]]))              # 1
    print(solver.minMeetingRooms([[1, 3], [3, 5]]))               # 1
```

---

## 🧪 Dry Run | 手動追蹤

**Input:** `[[4,9],[2,15],[9,29],[16,23],[36,45]]`

| Step | Action | Heap State |
|---|---|---|
| Init | Sort → `[[2,15],[4,9],[9,29],[16,23],[36,45]]`, push `15` | `[15]` |
| i=1 `[4,9]` | 4 >= 15? ❌ → push 9 | `[9, 15]` |
| i=2 `[9,29]` | 9 >= 9? ✅ → replace 9 with 29 | `[15, 29]` |
| i=3 `[16,23]` | 16 >= 15? ✅ → replace 15 with 23 | `[23, 29]` |
| i=4 `[36,45]` | 36 >= 23? ✅ → replace 23 with 45 | `[29, 45]` |
| **Return** | `len([29, 45])` | **2** |

---

## 🐛 Common Bugs to Avoid | 常見錯誤

| Bug | Fix |
|---|---|
| `intervals.sort()` — mutates input | Use `sorted(intervals, key=lambda x: x[0])` |
| `sorted(sort_intervals, ...)` — NameError before assignment | Use the original parameter name `intervals` on the right-hand side |
| Method name mismatch in test | Always match call site to the defined method name |
| Debug comments `# Fix #1` left in code | Strip all debug artifacts before submission |

---

## 📊 Final Evaluation | 最終評估

**Overall Rating / 總體評級:** `Lean Hire`

| Dimension | Feedback |
|---|---|
| **Clarification** | ✅ Strong — asked boundary condition and mutability upfront |
| **Algorithm** | ✅ Correctly identified min-heap without hints |
| **Code Quality** | ⚠️ Required 3 submissions to reach clean code |
| **Dry Run** | ✅ Flawless step-by-step trace |
| **Self-contradiction** | ❌ Negotiated read-only, then immediately called `intervals.sort()` |

### Actionable Corrections | 改善建議
1. **Read your own code top-to-bottom before submitting.** Catch NameErrors before the interviewer does.
   **提交前從頭到尾默讀自己的程式碼**，在面試官發現前先找到 NameError。
2. **Honour constraints you specify.** If you say "read-only", reflect it in your first draft.
   **遵守你自己協商的限制**，若說「唯讀」就在第一稿中反映出來。
3. **Submit clean code on the first attempt.** L5 standard = near-correct first draft.
   **第一次就提交乾淨的程式碼**。L5 標準 = 第一稿接近正確。
