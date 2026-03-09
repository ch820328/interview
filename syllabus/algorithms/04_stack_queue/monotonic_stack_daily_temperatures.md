# Monotonic Stack — Daily Temperatures (單調堆疊 — 每日溫度)

**Target Level / 目標等級:** Google L4 / L5
**Topic / 主題:** Monotonic Stack / 單調堆疊
**LeetCode:** #739 Daily Temperatures

---

## 1. Problem Statement + Constraints (題目與限制)

**English:**
Given an array of integers `temperatures`, return an array `answer` where `answer[i]` is the number of days after day `i` until a warmer temperature occurs. If no such day exists, `answer[i] = 0`. "Warmer" means strictly greater than (`>`).

**中文 (Chinese):**
給定一個整數陣列 `temperatures`，回傳一個陣列 `answer`，其中 `answer[i]` 代表在第 `i` 天之後需要等幾天才能遇到更高的溫度。若沒有更高溫度的天數，則 `answer[i] = 0`。「更高」的定義為嚴格大於（`>`）。

**Constraints / 限制:**
- `1 <= temperatures.length <= 10^5`
- `30 <= temperatures[i] <= 100`

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Does "warmer" mean strictly greater? / 「更高」是嚴格大於嗎？ | Yes, equal temperature does NOT count. / 是的，等溫不算。 |
| Can the array be empty? / 陣列可以為空嗎？ | Constraints say length ≥ 1, but code handles `[]` gracefully. / 限制為長度 ≥ 1，但程式碼能自然處理空陣列。 |
| Does temperature range affect the algorithm? / 溫度值的大小範圍影響算法嗎？ | No. Values are only used as comparison operands, not indices. / 不影響。溫度值僅用於比較，不用作索引。 |

---

## 3. Brute Force vs Optimal (暴力解 vs 最佳解)

| | Brute Force (暴力解) | Optimal — Monotonic Stack (最佳解 — 單調堆疊) |
|---|---|---|
| **Approach** | For each index `i`, scan all `j > i` until `temps[j] > temps[i]` | Maintain a stack of indices in **monotonically decreasing temperature** order |
| **方法** | 對每個 index `i`，向後掃描直到找到更高溫度 | 維護一個溫度**單調遞減**的 index 堆疊 |
| **Time Complexity** | O(n²) | O(n) — each index pushed & popped at most once |
| **時間複雜度** | O(n²) | O(n) — 每個 index 最多被 push/pop 各一次 |
| **Space Complexity** | O(1) auxiliary + O(n) output | O(n) stack + O(n) output |
| **空間複雜度** | O(1) 輔助空間 + O(n) 輸出 | O(n) 堆疊 + O(n) 輸出 |

**Key Insight / 關鍵洞察:**
EN: The stack stores indices (not values) so we can compute the day distance directly. The monotonic decreasing invariant ensures every element is processed at most twice.
ZH: 堆疊存 index（而非溫度值），讓我們可以直接計算天數差距。單調遞減的 invariant 保證每個元素最多被處理兩次。

---

## 4. Python Code Sample (Python 程式碼範例)

```python
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # Initialize result array with 0s (default: no warmer day found)
        # 初始化結果陣列為 0（預設：找不到更高溫的天）
        nextHigherTemperature = [0] * len(temperatures)
        
        # Monotonic decreasing stack of indices
        # 存放 index 的單調遞減堆疊
        stack = []

        for cur_day, cur_temp in enumerate(temperatures):
            # While stack is not empty AND current temp is higher than temp at stack top
            # 當堆疊非空，且當前溫度高於堆疊頂端的溫度時
            while stack and temperatures[stack[-1]] < cur_temp:
                pre_day = stack.pop()
                nextHigherTemperature[pre_day] = cur_day - pre_day  # distance in days / 天數差
            stack.append(cur_day)

        return nextHigherTemperature


# --- Test harness (測試) ---
if __name__ == "__main__":
    sol = Solution()
    print(sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))  # Normal case / 正常情況  → [1, 1, 4, 2, 1, 1, 0, 0]
    print(sol.dailyTemperatures([30, 40, 50, 60]))                  # All increasing / 全遞增  → [1, 1, 1, 0]
    print(sol.dailyTemperatures([30]))                               # Single element / 單一元素 → [0]
    print(sol.dailyTemperatures([90, 80, 70, 60]))                   # All decreasing / 全遞減  → [0, 0, 0, 0]
```

---

## 5. Step-by-Step Dry Run (逐步模擬)

Input: `temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`

| Day (天) | Temp (溫度) | Stack Before While (進入 while 前堆疊) | Stack After (while 後堆疊) | Result Updated (更新結果) |
|---|---|---|---|---|
| 0 | 73 | `[]` | `[0]` | — |
| 1 | 74 | `[0]` | `[1]` | `res[0] = 1-0 = 1` |
| 2 | 75 | `[1]` | `[2]` | `res[1] = 2-1 = 1` |
| 3 | 71 | `[2]` | `[2, 3]` | — |
| 4 | 69 | `[2, 3]` | `[2, 3, 4]` | — |
| 5 | 72 | `[2, 3, 4]` | `[2, 5]` | `res[4]=1, res[3]=2` |
| 6 | 76 | `[2, 5]` | `[6]` | `res[5]=1, res[2]=4` |
| 7 | 73 | `[6]` | `[6, 7]` | — |

**Final output / 最終結果:** `[1, 1, 4, 2, 1, 1, 0, 0]` ✅

---

## 6. Common Bugs (常見錯誤)

| Bug (錯誤) | Why It Happens (原因) | Fix (修正) |
|---|---|---|
| Using `<=` instead of `<` in while condition | Misreads "warmer" as "≥" | Use strict `<` (temperatures[stack[-1]] < cur_temp) |
| 使用 `<=` 而非 `<` | 誤解「更高」為「≥」 | 使用嚴格 `<` |
| Storing values instead of indices | Can't compute day distance | Store `cur_day`, compute `cur_day - pre_day` |
| 存溫度值而非 index | 無法計算天數差 | 存 `cur_day`，計算 `cur_day - pre_day` |
| Off-by-one when initializing result | Using wrong default | Initialize with `[0] * n`; unresolved stack entries default to 0 |
| 初始化結果陣列的 off-by-one | 使用錯誤的預設值 | 以 `[0] * n` 初始化；堆疊中未被 pop 的 index 結果自動為 0 |
| Forgetting `stack` check in while condition | `IndexError` on empty stack | Always write `while stack and ...` |
| 忘記在 while 條件中檢查堆疊是否為空 | 空堆疊導致 `IndexError` | 永遠寫成 `while stack and ...` |

---

## 7. Full Evaluation Rubric (完整評估表)

| Dimension (維度) | Rating (評分) | Notes (備註) |
|---|---|---|
| Overall / 總評 | **Lean Hire** | Correct solution, communication gaps |
| Problem Solving / 解題 | ✅ Strong | Correct O(n) independently reached |
| Code Quality / 程式品質 | ✅ Good | Clean names, idiomatic Python; one NameError on first run |
| Complexity Analysis / 複雜度 | ⚠️ Weak | Not volunteered proactively; had to be prompted |
| Dry Run / 模擬追蹤 | ✅ Excellent | Flawless step-by-step trace |
| Communication / 溝通 | ❌ Weak | One-line answers, no justification, switched to Chinese under pressure |
| Edge Cases / 邊界情況 | ✅ Handled | Empty array and large temperature range both addressed (when prompted) |

---

## 8. Actionable Corrections (改進建議)

**English:**
1. **Always present Brute Force first** — Frame it as: *"A naive O(n²) solution would be... but we can do better."* Never open with the optimal.
2. **Volunteer complexity unprompted** — End every approach with: *"This gives us O(n) time and O(n) space."*
3. **Explain reasoning in full English sentences** — *"It doesn't affect"* is not an answer. State why.
4. **Trace through code mentally before running** — Catch `NameError`-level bugs before the compiler does.

**中文:**
1. **永遠先提暴力解** — 格式：「最直覺的 O(n²) 解法是⋯⋯但我們可以做得更好。」絕不以最佳解開場。
2. **主動說明複雜度** — 每個方法結尾都應附上：「這給我們 O(n) 的時間複雜度和 O(n) 的空間複雜度。」
3. **用完整的英文句子解釋推論** — 「不影響」不是答案，要說清楚**為什麼**不影響。
4. **執行前先心算** — 在依賴編譯器之前，先用眼睛追蹤程式碼至少一次，找出 `NameError` 等低級錯誤。

---

## 9. Technical Term Dictionary / Glossary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Monotonic Stack** | A stack that maintains elements in strictly increasing or decreasing order | 單調堆疊：一個始終維持元素嚴格遞增或遞減順序的堆疊 |
| **Invariant** | A condition that remains true throughout the execution of an algorithm | 不變量：在演算法執行過程中始終保持成立的條件 |
| **Auxiliary Space** | Memory used by the algorithm beyond the input and output arrays | 輔助空間：除輸入和輸出陣列外，演算法額外使用的記憶體 |
| **Enumerate** | Python built-in that yields (index, value) pairs from an iterable | Python 內建函式，從可迭代物件中產生 (索引, 值) 的配對 |
| **Amortized O(n)** | Each element is processed a bounded number of times across all operations | 均攤 O(n)：每個元素在所有操作中被處理的次數是有限的 |
| **Edge Case** | An input at the boundary of constraints (e.g., empty array, single element, all decreasing) | 邊界情況：位於限制邊緣的輸入（如空陣列、單一元素、全遞減） |
| **STAR Method** | Not applicable here — coding rubric dimension | 不適用於此 — 為行為面試的評估框架 |
