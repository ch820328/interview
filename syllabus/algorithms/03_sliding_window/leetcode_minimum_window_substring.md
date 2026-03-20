# Minimum Window Substring / 最小涵蓋子字串

## Problem Statement / 題目描述
Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `""`.
給定兩個字串 `s` 和 `t`，長度分別為 `m` 和 `n`。請回傳 `s` 中最小涵蓋子字串，使得這個子字串包含 `t` 中所有的字元（包括重複字元）。如果沒有這樣的子字串，請回傳空字串 `""`。

### Constraints / 限制條件
- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.
- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` 和 `t` 僅由英文字母大小寫組成。

## Clarification Q&A / 釐清問題與解答
**Q:** If `t` is "AA", does the window need two 'A's?
**問:** 如果 `t` 是 "AA"，視窗是否需要兩個 'A'？
**A:** Yes, duplicate characters in `t` must be fully matched.
**答:** 是的，`t` 中的重複字元必須被完全匹配。

**Q:** What to return if no such string exists?
**問:** 如果不存在這樣的字串，該回傳什麼？
**A:** Return the empty string `""`.
**答:** 回傳空字串 `""`。

## Brute Force vs Optimal / 暴力法與最佳化比較

| Approach (方法) | Time Complexity (時間複雜度) | Space Complexity (空間複雜度) | Description (說明) |
|---|---|---|---|
| **Brute Force (暴力法)** | O(m * n) or O(n^3) | O(k) | Check every possible substring pair (left, right) to see if it contains `t`. / 檢查每一個可能的子字串區間 (left, right) 看是否包含 `t`。 |
| **Sliding Window (滑動視窗)** | O(m + n) | O(k) | Use two pointers to expand the window until valid, then shrink to find the minimum length. / 使用雙指針擴展視窗直到合法，然後縮小以尋找最小長度。 |

## Python Code Sample / 程式碼範例

```python
from typing import List
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        # Dictionary to keep track of character counts in t
        t_count = Counter(t)
        t_char_need = len(t_count.keys())

        min_length = float('inf')
        min_length_string = ''
        left = 0
        
        for right in range(len(s)):
            if s[right] in t_count:
                t_count[s[right]] -= 1
                if t_count[s[right]] == 0:
                    t_char_need -= 1
                
                # Window is valid, try to shrink it
                while t_char_need == 0:
                    if min_length > right - left + 1:
                        min_length = right - left + 1
                        min_length_string = s[left:right + 1]
                        
                        # Optimization: if length equals len(t), it's the absolute minimum
                        if min_length == len(t):
                            return min_length_string
                            
                    if s[left] in t_count:
                        t_count[s[left]] += 1
                        if t_count[s[left]] == 1:
                            t_char_need += 1
                    left += 1
                    
        return min_length_string

# --- Test harness (測試) ---
if __name__ == "__main__":
    sol = Solution()
    print(sol.minWindow("ADOBECODEBANC", "ABC"))  # Normal case / 正常情況, Expected: "BANC"
    print(sol.minWindow("a", "a"))                # Small input / 單量輸入, Expected: "a"
    print(sol.minWindow("ABCzzzzBANC", "ABC"))    # Edge case / 邊界情況, Expected: "ABC"
```

## Step-by-step Dry Run / 逐步執行追蹤

| Step (步驟) | Left | Right | s[right] | Window (視窗) | t_char_need | Action (動作) |
|---|---|---|---|---|---|---|
| Expand (擴展) | 0 | 2 | C | "ABC" | 0 | Window valid. Update min to 3. Return early. / 視窗合法。更新最小值為 3。提早回傳。|
*(Trace based on the `ABCzzzzBANC` example early return optimization)*
*(基於 `ABCzzzzBANC` 範例提早回傳優化的追蹤)*

## Common Bugs / 常見錯誤

| Bug (錯誤) | Consequence (後果) | Prevention (預防) |
|---|---|---|
| Forgetting to update `min_length` inside the `while` loop. | Returns the last valid window checked instead of the globally minimum window. | Always track and update the actual length variable alongside the string variable. |
| 忘記在 `while` 迴圈內更新 `min_length`。 | 回傳最後一個檢查的合法視窗，而非全域最小的視窗。 | 永遠在更新字串變數的同時，追蹤並更新實際的長度變數。 |
| Using `O(N)` check for dictionary equality inside the window. | Degrades the sliding window time from `O(N)` to `O(N * K)`. | Use a single `need` counter variable to track fulfilled characters. |
| 在視窗內使用 `O(N)` 來檢查字典是否相等。 | 將滑動視窗時間從 `O(N)` 降級為 `O(N * K)`。 | 使用單一 `need` 計數器變數來追蹤已滿足的字元數。 |

## Full Evaluation Rubric / 完整評分標準

- **Strong Hire (強烈錄取)**: Spotless optimal implementation in ~15 mins with robust testing and correct handling of streaming data conceptual questions.
- **強烈錄取**: 在約 15 分鐘內完成無瑕疵的最佳化實作，包含穩健的測試並正確回答串流資料的概念性問題。
- **Hire (錄取)**: Optimal solution with minor hints. Clear communication of time/space complexity.
- **錄取**: 在少量提示下完成最佳解。清楚溝通時間與空間複雜度。
- **Lean Hire (勉強錄取)**: Requires multiple hints to fix bugs like forgetting to update `min_length`.
- **勉強錄取**: 需要多個提示來修復錯誤（例如忘記更新 `min_length`）。
- **No Hire (不錄取)**: Fails to find optimal, brute-force only, or relying on external AI assistance.
- **不錄取**: 未能找到最佳解，僅依靠暴力法，或依賴外部 AI 輔助。

## Actionable Corrections / 具體改進建議

1. **Always write down variable values when dry-running instead of assuming code does what you meant it to do.**
1. **手動追蹤程式碼時，永遠寫下變數的值，而不是假設程式碼會照你的想法運作。**
2. **Never use external GenAI tools during a real assessment.**
2. **絕對不要在真實的面試評估過程中使用外部的生成式 AI 工具。**

## Technical Term Dictionary / 技術術語字典
- **Sliding Window (滑動視窗)**: An algorithm pattern that maintains a subset of items to reduce the use of nested loops and decrease time complexity. / 一種演算法模式，透過維護一個集合的子區間來減少嵌套迴圈的使用並降低時間複雜度。
- **Time Complexity (時間複雜度)**: The computational complexity that describes the amount of time it takes to run an algorithm. / 描述演算法執行所需時間的計算複雜度。
- **Space Complexity (空間複雜度)**: The amount of memory space required to solve an instance of the computational problem as a function of the input size. / 解決計算問題所需的記憶體空間量，作為輸入大小的函數。
- **Hash Map / Dictionary (雜湊表 / 字典)**: A data structure that implements an associative array abstract data type, a structure that can map keys to values. / 實作關聯陣列抽象資料型別的資料結構，一種可以將鍵映射到值的結構。
- **Early Return (提早回傳)**: A pattern where a function exits early if a specific condition is met, saving unnecessary computation. / 一種模式，如果滿足特定條件，函式會提早結束，節省不必要的運算。
