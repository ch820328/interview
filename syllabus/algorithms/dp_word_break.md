# Algorithm Deep Dive: Dynamic Programming & Loop Optimization (Word Break)
# 演算法深潛：動態規劃與迴圈優化 (單詞拆分)

**Target Level (目標職級):** Google L4 / L5 (Senior Software Engineer)
**Focus Area (核心考點):** DP State Transition, Overlapping Subproblems, Constraints-Driven Optimization

---

## 📝 The Problem: Word Break (單詞拆分)

**English:**
Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words. Note that the same word in the dictionary may be reused multiple times.

**Chinese (中文):**
給定一個字串 `s` 和一個字串字典 `wordDict`，請判斷字串 `s` 是否可以被完全拆分成一個或多個在字典中出現過的單詞。字典中的同一個單詞可以被重複使用多次。

**Constraints (限制條件):**
* `1 <= s.length <= 300`
* `1 <= wordDict.length <= 1000`
* `1 <= wordDict[i].length <= 20`

---

## 🧠 L5 Algorithm Breakdown (L5 演算法拆解)

### 1. Why Not Two-Pointer / Bidirectional? (為何不用雙向夾擠？)
**English:**
A naive approach might try to match words from the front and the back simultaneously. However, this fails on combinatorial edge cases like `s = "aaaaaaa"` with `wordDict = ["a", "aa", "aaaa"]`. Without memorizing previous results, a bidirectional search degrades into an exponential BFS/Backtracking algorithm, causing a Time Limit Exceeded (TLE).

**Chinese (中文):**
直覺上可能會想用雙向指標從頭尾同時配對單字。但遇到像 `s = "aaaaaaa"` 且字典是 `["a", "aa", "aaaa"]` 這種充滿頻繁組合的極端測資時，雙向搜尋（若沒有紀錄子問題結果）會退化成指數等級 $O(2^N)$ 的回溯法，直接導致 TLE (超時)。

### 2. The 1D DP State Transition (1D 動態規劃狀態轉移)
**English:**
- **State Definition:** `dp[i]` is a boolean representing whether the prefix `s[0:i]` can be segmented into dictionary words.
- **Base Case:** `dp[0] = True` (an empty string is valid).
- **Transition Formula:** `dp[i] = dp[j] and s[j:i] in wordSet` for some `0 <= j < i`.

**Chinese (中文):**
- **狀態定義：** `dp[i]` 是一個布林值，代表字串 `s` 的前 `i` 個字元能否合法拆分。
- **初始狀態：** `dp[0] = True` (空字串合法)。
- **轉移方程式：** 只要存在一個斷點 `j`，使得 `dp[j] == True` 且後綴 `s[j:i]` 也存在於字典中，那麼 `dp[i]` 就是 `True`。

---

## 💣 The L5 Constraint Trick: Max-Length Optimization (L5 極限長度優化)

**English:**
A standard implementation sets up two loops: an outer loop `i` from `1` to `len(s)`, and an inner loop `j` from `0` to `i`. This yields $O(N^2)$ time.
However, a Senior engineer will look at the constraints: `wordDict[i].length <= 20`. 
If `i - j > 20`, checking `s[j:i]` in the set is mathematically useless because no word in the dictionary is that long. We should bound the inner loop's look-back length to `max_len`, reducing the inner iterations from $O(N)$ to a constant $O(20)$.

**Chinese (中文):**
標準的 DP 寫法會用雙層迴圈，讓 `i` 跑到字串尾，`j` 從 `0` 跑到 `i`，這會產生 $O(N^2)$ 的時間複雜度。
但資深工程師會敏銳地抓住限制條件：**「字典裡最長的單字不超過 20 個字元」**。
當 `i - j > 20` 時，去字典裡找這個超長字串純粹是浪費 CPU 運算。所以我們應該把內迴圈「往回看」的跨度限制在字典的 `max_len` (通常是 20)，把內迴圈從 $O(N)$ 直接降維打擊成常數時間的 $O(20)$ 甚至更小。

---

## 💻 The Ultimate L5 Code Template (L5 終極程式碼模板)

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        # Convert list to set for O(1) lookups
        # 將字典轉為 Set，將查找時間降至 O(1)
        wordSet = set(wordDict)
        
        # L5 Constraint Awareness: Find the maximum word length
        # L5 優化：找出字典中最長單字的長度
        max_len = max(len(w) for w in wordDict)
        
        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True
        
        for i in range(1, n + 1):
            # Optimization: j only needs to look back up to max_len
            # 優化：j 最多只需要往回看 max_len 的長度
            start_j = max(0, i - max_len)
            
            for j in range(start_j, i):
                if dp[j] and s[j:i] in wordSet:
                    dp[i] = True
                    break # Stop checking further if we already found a valid cut
                    
        return dp[n]
```

### 📉 Complexity Analysis (複雜度分析)
**English:**
* **Time Complexity:** $O(N \cdot \max(L) + M \cdot \max(L))$ where $N$ is the length of string `s`, $\max(L)$ is the maximum length of a word in `wordDict`, and $M$ is the number of words in `wordDict`. Thanks to the look-back optimization, the DP loop runs in $O(N \cdot \max(L))$. Converting the dictionary to a set takes $O(M \cdot \max(L))$. Total time limits to $O(N \cdot 20) \approx O(N)$.
* **Space Complexity:** $O(N + M \cdot \max(L))$ for the DP array of size $N$ and the Hash Set storing $M$ dictionary words.

**Chinese (中文):**
* **時間複雜度：** $O(N \cdot \max(L) + M \cdot \max(L))$，其中 $N$ 是字串長度，$\max(L)$ 是字典中最長單字的長度，$M$ 是字典單字總數。因為有了極限長度限制優化，DP 內迴圈的執行次數被死死卡在常數級別 (20以內)，實際上接近 $O(N)$。
* **空間複雜度：** $O(N + M \cdot \max(L))$。需要一個長度為 $N$ 的 DP 陣列來紀錄狀態，以及需要儲存總字串長度的 Hash Set。
