# Coding Interview: Buddy Strings (字串夥伴)

**Topic / 主題:** String Manipulation & Counting / 字串操作與計數
**Difficulty / 難度:** Easy-Medium (LeetCode 859)
**Target Level / 目標等級:** Google L4
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-11

---

## 1. Problem Statement (題目)

**English:**
Given two strings `s` and `goal`, return `true` if you can swap two letters in `s` so the result is equal to `goal`. Swapping exactly one pair of indices is mandatory.

**中文：**
給定兩個字串 `s` 和 `goal`，如果可以透過交換 `s` 中的兩個字母來使其等於 `goal`，則回傳 `true`。必須恰好進行一次交換。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Mandatory swap? / 必須交換嗎？ | Yes, even if `s == goal`. / 是的，即使一開始就相等也得換。 |
| Character set? / 字元集？ | Lowercase `a-z` only. / 僅限小寫 a-z。 |
| Empty or different length? / 空字串或長度不同？ | Return `false`. / 回傳 `false`。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Early Exit (Length)** | If lengths differ, a swap can never make them equal. / 若長度不同，絕對無法透過交換相等。 |
| **Identical Case (s == goal)** | To swap and remain equal, `s` must have at least one character repeating (e.g., "aba" -> swap 'a's -> "aba"). / 若字串相同，必須有重複字母（鴿籠原理）才能在交換後保持不變。 |
| **Differing Case (s != goal)** | Find all indices where `s[i] != goal[i]`. There must be exactly 2 such indices, and `s[i] == goal[j]` and `s[j] == goal[i]`. / 找出所有不同位元。必須恰好有 2 個不同位元，且交叉相等。 |

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
class Solution:
    def buddyStrings(self, s: str, goal: str) -> bool:
        # Base check
        if len(s) != len(goal):
            return False
            
        # Case 1: Strings are already identical
        if s == goal:
            # Check for at least one duplicate character
            # O(N) time, O(1) space (at most 26 chars)
            seen = set()
            for char in s:
                if char in seen:
                    return True
                seen.add(char)
            return False
        
        # Case 2: Strings differ
        # Track mismatch indices. Early exit if more than 2.
        mismatches = []
        for i in range(len(s)):
            if s[i] != goal[i]:
                mismatches.append(i)
                if len(mismatches) > 2:
                    return False
        
        # Must have exactly 2 mismatches that can be swapped
        if len(mismatches) != 2:
            return False
            
        i, j = mismatches
        return s[i] == goal[j] and s[j] == goal[i]
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Time / 時間** | **O(N)** | Single pass through the string of length N. / 對長度 N 的字串進行一次遍歷。 |
| **Space / 空間** | **O(1)** | The `seen` set stores at most 26 lowercase English letters. / `seen` 集合最多儲存 26 個小寫字母。 |

---

## 6. Actionable Corrections (改進行動)

**English:**
1. **Early Exit Optimization:** Adding `if len(mismatches) > 2: return False` is a professional touch reflecting production-aware coding (don't waste cycles on unsalvageable cases).
2. **Pigeonhole Principle:** Realize that `s == goal` needs a duplicate—this is a common trap for candidates who forget about the mandatory swap requirement.

**中文：**
1. **提早結束優化：** 加入 `len(mismatches) > 2` 直接回傳是展現「具備產品開發意識」的細節，能避免在無法修補的情況下浪費計算資源。
2. **鴿籠原理：** 意識到 `s == goal` 時需要有重複字母，這是針對「強制交換」條件的常見陷阱。

---

## 7. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Early Exit** | Stopping a process as soon as a condition for failure/success is met | 提早結束 / 提早退出 |
| **Single Pass** | Iterating through a collection exactly once | 一次遍歷 |
| **Pigeonhole Principle** | If n items are put into m containers, and n > m, at least one container has >1 item | 鴿籠原理 |
| **Mismatch** | A position where two elements in a sequence do not align | 不匹配 / 差異位元 |
| **Index Mapping** | Swapping values at specific memory locations (indices) | 索引映射 / 交換 |
