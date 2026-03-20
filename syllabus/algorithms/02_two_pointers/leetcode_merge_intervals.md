# Algorithm Deep Dive: Merge Intervals (區間合併)

**Target Level:** Google L4 / L5 (Senior Software Engineer)
**Focus Area:** Array Processing, Sorting, In-place vs Immutable Operations, Edge Cases (Full Inclusion)

---

## 📝 The Problem

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.

**Example:**
```text
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
```

---

## 🧠 L5 Algorithm Breakdown

### 1. The Pre-processing (Sorting)
Interval problems are extremely difficult to solve in $O(N^2)$ without sorting. 
**The Golden Rule:** Always sort the intervals by their `start` time.
Once sorted, you guarantee that for any interval $i$ and $i+1$, the start time of $i$ is always less than or equal to the start time of $i+1$. This reduces the overlap check to a simple sweeping line.

### 2. The L5 Trap: Input Data Mutation (Side-effects)
**Novice Approach:** `intervals.sort()`
In a production system, `intervals` might be a reference passed from another module. Sorting it in place mutates the original data, which can cause subtle, catastrophic bugs elsewhere in the system.
**Senior Approach:** Ask the interviewer if modifying the input is allowed. If not (or by default in functional programming paradigms), use `sorted(intervals)` to create an immutable copy.

### 3. The L5 Trap: Full Inclusion (大區間吃小區間)
When merging, it is not enough to just take the `end` of the current interval.
Consider: `prev = [1, 10]`, `curr = [2, 5]`.
If you blindly merge by taking `curr[1]`, the merged interval becomes `[1, 5]`, which incorrectly shrinks the interval.
**Solution:** Always use `max(prev_end, curr_end)` to dictate the new right boundary.

### 4. Code Redundancy (Trusting Your Invariants)
Because the array is sorted by start time, when you process `raws[i]`, you *already know* that `raws[i][0] >= current_start`. 
Writing `if current_start <= raws[i][0] <= current_end:` is redundant and shows a lack of confidence in the sorted invariant. 
**Simply write:** `if raws[i][0] <= current_end:`

---

## 💻 The Ultimate L5 Code Template

```python
class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        if not intervals:
            return []
            
        # L5: Avoid mutating the input argument by creating a sorted copy
        raws = sorted(intervals)
        res = []
        
        start, end = raws[0]
        
        for i in range(1, len(raws)):
            # L5: Trust the sorted invariant. We only need to check against 'end'
            if raws[i][0] <= end:
                # L5: Edge Case Defense - Full Inclusion [1, 10] and [2, 5]
                end = max(end, raws[i][1])
            else:
                # No overlap, push the confirmed interval
                res.append([start, end])
                # Reset the tracking variables
                start, end = raws[i]
        
        # Pythonic: 'for...else' or simply appending the final tracked interval 
        # outside the loop ensures the last piece is never dropped.
        res.append([start, end])

        return res
```

### 📉 Complexity Analysis
*   **Time Complexity:** $O(N \log N)$. The completely dominant factor is the `sorted()` operation. The linear scan takes $O(N)$, which is overshadowed.
*   **Space Complexity:** $O(N)$. We allocate $O(N)$ space for the `raws` array (assuming $O(N)$ for Python's Timsort overhead and the duplicated array to preserve immutability) and $O(N)$ for the `res` output array in the worst case (no overlaps).
