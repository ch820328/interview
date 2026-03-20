# Coding Interview: Word Guessing Strategy (猜字策略)

**Topic / 主題:** Filtering & Heuristics / 資料過濾與啟發式搜索
**Difficulty / 難度:** Hard (LeetCode 843 variant)
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Hire**
**Session Date / 面試日期:** 2026-03-10

---

## 1. Problem Statement (題目)

**English:**
You are given a dictionary of 5-letter words with no duplicate letters. A secret word exists in the dictionary. You can call `guess(word)` which returns the number of exact character matches (Green). Find the secret word in as few attempts as possible (typically under 10).

**中文：**
給定一個字典，包含長度為 5 且無重複字母的單字。字典中存在一個秘密單字。你可以呼叫 `guess(word)`，它會回傳精確匹配的字元數量（即 Green）。請用盡可能少的次數（通常在 10 次內）找到該秘密單字。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Score for misplaced characters? / 字元正確但位置錯誤有分數嗎？ | 0. We only count exact index matches. / 0 分。我們只計算索引完全相同的匹配。 |
| Character set? / 字元集為何？ | a-z lowercase only. / 僅限 a-z 小寫。 |
| Can I guess any word? / 可以猜任何字嗎？ | No, only words in the dictionary are allowed. / 不行，只能猜測字典內的單字。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Consistency Filtering** | If `guess(G)` is `v`, the secret word `S` must satisfy `matches(S, G) == v`. Prune all candidates that don't satisfy this. / 如果猜測 `G` 得到 `v` 分，秘密單字 `S` 必須滿足 `matches(S, G) == v`。刪除所有不符合此條件的候選單字。 |
| **Frequency Heuristic** | To pick the best `G`, count the frequency of each char at each position across candidates. Pick the word with the highest "popularity" score. / 為了挑選最佳的 `G`，計算所有候選單字在每個位置上的字元頻率。挑選「大眾臉」（字元頻率總和最高）的單字。 |
| **Why Frequency?** | A "popular" word is more likely to yield a non-zero score, providing more information for pruning. / 一個具備大眾特徵的單字更有可能獲得非 0 分，從而提供更多的過濾資訊。 |

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
from typing import List

class Solution:
    def findSecretWord(self, wordlist: List[str], master: 'Master') -> None:
        candidates = list(wordlist)
        
        while candidates:
            # Selection Strategy: most central/popular word
            guess_word = self.get_best_guess(candidates)
            score = master.guess(guess_word)
            
            if score == 5:
                return
            
            # Consistency Pruning
            candidates = [w for w in candidates if self.get_matches(w, guess_word) == score]

    def get_matches(self, s1: str, s2: str) -> int:
        return sum(1 for a, b in zip(s1, s2) if a == b)

    def get_best_guess(self, candidates: List[str]) -> str:
        if not candidates: return ""
        
        # Position-based character frequency count
        counts = [{} for _ in range(5)]
        for word in candidates:
            for i, char in enumerate(word):
                counts[i][char] = counts[i].get(char, 0) + 1
        
        # Score words by summing popularity of its characters
        best_word = candidates[0]
        max_score = -1
        
        for word in candidates:
            word_score = sum(counts[i][char] for i, char in enumerate(word))
            if word_score > max_score:
                max_score = word_score
                best_word = word
                
        return best_word
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Time / 時間** | **O(G × N)** | G is number of guesses (avg 4-6), N is dictionary size. Each guess filters N candidates in O(1) per word. / G 為猜測次數，N 為字典大小。每次猜測都在線性時間內過濾。 |
| **Space / 空間** | **O(N)** | Tracking candidates list. / 儲存候選清單。 |

---

## 6. Actionable Corrections (改進行動)

**English:**
1. **Minimax Strategy (L5+):** In a real interview, mention **Minimax** as the gold standard (pick word that minimizes the maximum possible remaining candidate set size). Frequency is a great $O(N)$ approximation, but Minimax is $O(N^2)$.
2. **Be Careful with 0-score:** If you get score 0, it is **extremely powerful**. It prunes all words that have ANY match with the guess. Mentioning this during the interview shows deep insight into the filtering logic.

**中文：**
1. **Minimax 策略 (L5+):** 在面試中，可以提及 **Minimax** 作為黃金標準（挑選那一個不論結果如何都能使剩餘集合儘量小的單字）。頻率法是極佳的 $O(N)$ 近似，但 Minimax 是 $O(N^2)$。
2. **注意 0 分的效力：** 得到 0 分是非常強大的過濾條件。它會刪除所有跟該猜測有「任何」重疊的單字。在面試中提及這點能展現你對過濾邏輯的深刻理解。

---

## 7. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Consistency Principle** | A logic where potential solutions must behave like the proven part | 一致性原則 |
| **Pruning** | Removing branches or items from a search space | 剪枝 |
| **Heuristic** | A rule of thumb to find a good but not necessarily optimal solution | 啟發式搜索 |
| **Information Gain** | The reduction in uncertainty after receiving new data | 資訊增益 |
| **Probability Distribution** | How likely each score (0 to 5) is for a given guess | 機率分佈 |
