# Coding Interview: Sliding Window Maximum (滑動視窗最大值)

**Topic / 主題:** Monotonic Deque / 單調隊列
**Difficulty / 難度:** Medium-Hard (LeetCode ~239 variant)
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Hire**
**Session Date / 面試日期:** 2026-03-09

---

## 1. Problem Statement (題目)

**English:**
Given an integer array `nums` and integer `k`, return the **minimum** of the **maximum values** across all contiguous subarrays of length `k`.

**中文:**
給定一個整數陣列 `nums` 和整數 `k`，回傳所有長度為 `k` 的連續子陣列中，各子陣列**最大值**的**最小值**。

**Constraints / 限制條件:**
```
1 ≤ k ≤ nums.length
1 ≤ nums.length ≤ 10^5
-10^4 ≤ nums[i] ≤ 10^4
```

**Example / 範例:**
```
Input:  nums = [1, 3, 1, 2, 0, 5], k = 3
Output: 2

Subarrays / 子陣列:
  [1,3,1] → max = 3
  [3,1,2] → max = 3
  [1,2,0] → max = 2  ← minimum of all maximums / 最小的最大值
  [2,0,5] → max = 5
```

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Can k be 0 or negative? / k 可以是 0 或負數嗎？ | No. 1 ≤ k ≤ nums.length / 不行 |
| Can k exceed nums.length? / k 可以超過陣列長度嗎？ | No. Guaranteed valid / 保證合法 |
| Can nums be empty? / nums 可以是空的嗎？ | No. 1 ≤ nums.length / 不行 |
| Range of values? / 數值範圍？ | -10^4 ≤ nums[i] ≤ 10^4 |

---

## 3. Brute Force vs Optimal (暴力法 vs 最佳解)

| Approach (方法) | Time (時間) | Space (空間) | Key Idea (核心思路) |
|---|---|---|---|
| **Brute Force** | O(n·k) | O(1) | For each window start, call `max()` on slice / 對每個視窗呼叫 `max()` |
| **Monotonic Deque** | O(n) | O(k) | Deque stores indices in decreasing value order; front = window max / 隊列維持遞減索引，前端為視窗最大值 |

**Bottleneck of Brute Force / 暴力法瓶頸:**
Each element is re-examined k times across overlapping windows. The monotonic deque eliminates this by processing each element **at most once** (push once, pop once).

每個元素在重疊視窗中被重複檢查 k 次。單調隊列透過讓每個元素**最多被 push/pop 各一次**來消除此重複。

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
from typing import List
from collections import deque

class Solution:
    def minMaxSubarray(self, nums: List[int], k: int) -> int:
        res = float('inf')
        data = deque()  # stores indices / 儲存索引

        for idx, num in enumerate(nums):
            # Remove from back: keep deque decreasing (by value)
            # 從後端移除：保持隊列數值遞減
            # Use <= so equal elements keep the most recent index (correct expiry)
            # 使用 <= 讓相等元素保留最新索引（確保正確的過期判斷）
            while data and nums[data[-1]] <= num:
                data.pop()
            data.append(idx)

            # Remove from front: evict indices outside the current window [idx-k+1, idx]
            # 從前端移除：驅逐超出當前視窗 [idx-k+1, idx] 的索引
            if data[0] <= idx - k:
                data.popleft()

            # Record result once a full window is formed
            # 視窗滿 k 個元素後才記錄結果
            if idx >= k - 1:
                res = min(res, nums[data[0]])

        return res


# --- Test harness (測試) ---
if __name__ == "__main__":
    sol = Solution()
    print(sol.minMaxSubarray([1, 3, 1, 2, 0, 5], 3))  # Expected: 2  (Normal / 正常)
    print(sol.minMaxSubarray([1, 1, 1, 1], 2))          # Expected: 1  (All equal / 全相等)
    print(sol.minMaxSubarray([5], 1))                    # Expected: 5  (Single element / 單元素)
    print(sol.minMaxSubarray([3, 1, 2, 5, 4], 3))       # Expected: 3  (Dry run case / Dry run 案例)
```

---

## 5. Step-by-Step Dry Run (逐步追蹤)

**Input:** `nums = [3, 1, 2, 5, 4]`, `k = 3`
**Expected:** `3`

| idx | num | Back-pop Logic | data (indices) | Front Expiry? | res |
|---|---|---|---|---|---|
| 0 | 3 | deque empty | [0] | No | inf |
| 1 | 1 | 3 > 1, keep | [0, 1] | No | inf |
| 2 | 2 | 1 ≤ 2 → pop 1; 3 > 2, stop | [0, 2] | 0 ≤ -1? No | min(inf, nums[0])=**3** |
| 3 | 5 | 2 ≤ 5 → pop 2; 3 ≤ 5 → pop 0 | [3] | 3 ≤ 0? No | min(3, nums[3])=**3** |
| 4 | 4 | 5 > 4, keep | [3, 4] | 3 ≤ 1? No | min(3, nums[3])=**3** |

**Return: 3** ✅

---

## 6. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Time / 時間** | **O(n)** | Each element is pushed **at most once** and popped **at most once** — amortized O(1) per element / 每個元素最多被 push 一次、pop 一次，均攤 O(1) |
| **Space / 空間** | **O(k)** | Deque holds at most k indices at any time / 隊列在任意時刻最多持有 k 個索引 |

> ⚠️ **Interview tip / 面試提醒:** Always justify O(n) with the push/pop argument, not just "scan once." / 永遠用「push/pop 各一次」來說明 O(n)，而非「只掃一遍」。

---

## 7. Common Bugs (常見錯誤)

| Bug (錯誤) | Root Cause (根本原因) | Fix (修正) |
|---|---|---|
| Using `<` instead of `<=` for back-pop | Older equal-value indices stay in deque, causing wrong expiry | Use `<=` to evict stale equal-value indices |
| 後端 pop 用 `<` 而非 `<=` | 相等值的舊索引殘留隊列，導致錯誤過期判斷 | 使用 `<=` 驅逐過期的相等值索引 |
| Storing values instead of indices | Cannot determine if front element has left the window | Store indices; compare `data[0] <= idx - k` |
| 儲存數值而非索引 | 無法判斷前端元素是否已離開視窗 | 儲存索引；比較 `data[0] <= idx - k` |
| Updating `res` before window is full | `res` gets values from partial windows | Guard with `if idx >= k - 1` |
| 視窗未滿就更新 `res` | `res` 從不完整視窗取值 | 加上 `if idx >= k - 1` 的保護條件 |

---

## 8. Follow-up: External Storage / Streaming (延伸題：外部儲存 / 串流)

**Q:** What if `nums` has 10^9 elements in external storage and can't fit in memory?

**Answer Framework / 解答框架:**

1. **Streaming Model (串流模型):** The monotonic deque is inherently an **online algorithm** — it needs only the last k elements, not the full array. Replace `List` input with an `Iterator` or stream interface.

   單調隊列本質上是**線上演算法**，僅需最近 k 個元素，無需完整陣列。將 `List` 輸入替換為 `Iterator` 或串流介面。

2. **Chunking + State Persistence (分塊 + 狀態持久化):** Load data in 64MB chunks. The deque state (indices + current global offset) must persist across chunks.

   分 64MB 塊載入資料。Deque 狀態（索引 + 全域偏移）需跨塊持久化。

3. **Large-k Problem (大 k 問題):** If k is also huge and the O(k) deque exceeds memory, use a **Block-based approach**: precompute max per block of size B; window max = left remainder + middle full-block maxima + right remainder. Memory drops from O(k) to O(n/B).

   若 k 也很大導致 O(k) 的 deque 超出記憶體，使用**分塊最大值法**：預先計算大小為 B 的塊的最大值；視窗最大值 = 左殘餘 + 中間完整塊最大值 + 右殘餘。記憶體從 O(k) 降為 O(n/B)。

4. **I/O Optimization (I/O 優化):** Use async prefetching — process current chunk while background thread reads the next.

   使用非同步預讀——處理當前塊時，背景執行緒已在讀取下一塊。

---

## 9. Full Evaluation Rubric (完整評估表)

| Dimension / 維度 | Rating / 評分 | Notes / 備註 |
|---|---|---|
| **Overall / 總評** | **Hire** | Clean optimal solution; follow-up was L5+ |
| **Brute Force** | ✅ Correct | O(n·k) / O(1), stated immediately |
| **Optimal Approach** | ✅ Derived Independently | No hints needed for deque insight |
| **Implementation** | ✅ Clean | Correct expiry, edge cases handled |
| **Dry Run** | ✅ Accurate | All index transitions traced correctly |
| **Complexity** | ⚠️ Incomplete | Correct answer, incomplete justification |
| **Edge Cases** | ⚠️ Unstated | `<=` choice not verbally explained |
| **Follow-up** | ✅ L5+ | Streaming, chunking, block-based max, async I/O |

---

## 10. Actionable Corrections (改進行動)

**English:**
1. **Justify O(n) precisely:** Always say *"each element is pushed at most once and popped at most once"* — this is the amortized argument, not just "scan once."
2. **Vocalize `<=` choice:** Explicitly state: *"I use `<=` so equal elements keep the most recent index, which gives correct window expiry."* Silence looks like luck.
3. **Structure follow-ups top-down:** State the streaming model first, then drill into chunk handling, then memory optimizations.

**中文:**
1. **精確說明 O(n)：** 永遠說「每個元素最多被 push 一次、pop 一次」——這是均攤論點，而非「只掃一遍」。
2. **說明 `<=` 的選擇：** 明確說明：「我使用 `<=` 是為了讓相等元素保留最新索引，確保視窗過期判斷正確。」沉默顯得像是運氣。
3. **延伸題由上而下展開：** 先說明串流模型，再說分塊處理，最後說記憶體優化。

---

## 11. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Monotonic Deque** | A deque that maintains elements in strictly increasing or decreasing order | 維持元素嚴格遞增或遞減順序的雙端隊列 |
| **Sliding Window** | A subarray that moves through the array one step at a time | 逐步在陣列中移動的子陣列視窗 |
| **Amortized O(1)** | An operation that may occasionally cost more, but averages to O(1) over all operations | 偶爾成本較高，但所有操作平均下來為 O(1) 的均攤分析 |
| **Online Algorithm** | An algorithm that processes input sequentially without needing future data | 不需要未來資料、依序處理輸入的演算法 |
| **Chunking** | Dividing large data into fixed-size blocks for sequential processing | 將大型資料切割為固定大小的塊以循序處理 |
| **Async Prefetching** | Loading the next data chunk in the background while processing the current chunk | 在處理當前塊時於背景載入下一塊資料 |
| **Block-based Max** | Precomputing max values per block to answer range-max queries efficiently | 預先計算每塊最大值以有效率地回應範圍最大值查詢 |
| **Front Expiry** | Removing the front deque element when its index falls outside the current window | 當前端元素的索引超出當前視窗時將其移除 |
