# Coding Interview: Word List Char Stream (字元流與字典清單)

**Topic / 主題:** Trie (Reversed) / 字典樹（反向）
**Difficulty / 難度:** Hard (LeetCode 1032)
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-11

---

## 1. Problem Statement (題目)

**English:**
Design a data structure that accepts a stream of characters one by one. After each character, check if any word from a given dictionary is a suffix of the current stream.

**中文：**
設計一個資料結構，逐一接收字元流。在每個字元輸入後，檢查字典中是否有任何單字是目前字元流的「後綴（Suffix）」。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Single or multi-char query? / 單次查詢是一個還是多個字元？ | Single character per `query(char)`. / 每次 `query(char)` 只接收一個字元。 |
| Suffix definition? / 後綴的定義？ | The word must end exactly at the current character. / 單字必須剛好結束於當前輸入的字元。 |
| Efficiency? / 效率要求？ | Words up to 200 chars. Queries up to 40k. Must be efficient. / 單字最長 200，查詢達 4 萬次。必須非常高效。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Reversed Trie** | Store all dictionary words in a Trie in **reversed order**. / 將字典中的所有單字以「反向」順序存入 Trie。 |
| **Stream History** | Maintain a `deque` of the last 200 characters received (since that's the max word length). / 維持一個 `deque` 儲存最近收到的 200 個字元（因為這是單字最大長度）。 |
| **Suffix as Prefix** | A suffix check in the stream becomes a **prefix check** in the Reversed Trie starting from the most recent character. / 對字元流的「後綴檢查」轉化為在反向 Trie 中從最新字元開始的「前置檢查」。 |
| **Early Exit** | If the stream character doesn't exist in the Trie node's children, return `False` immediately. / 如果字元流字元不在 Trie 節點的子節點中，立即回傳 `False`。 |

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
from collections import deque
from typing import List

class StreamChecker:
    def __init__(self, words: List[str]):
        # Build Trie with reversed words
        self.trie = {}
        for word in words:
            node = self.trie
            for char in reversed(word):
                if char not in node:
                    node[char] = {}
                node = node[char]
            node['#'] = True # End of word marker
        
        # History of the stream
        self.history = deque()
        self.max_len = 200 # Constraint: Max word length

    def query(self, letter: str) -> bool:
        self.history.appendleft(letter)
        if len(self.history) > self.max_len:
            self.history.pop()
            
        # Search in the reversed Trie
        node = self.trie
        for char in self.history:
            if char not in node:
                return False
            node = node[char]
            if '#' in node: # Found a word that is a suffix
                return True
        return False
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Init Time** | **O(N × L)** | N words, L max length. / N 個單字，L 為最大長度。 |
| **Query Time** | **O(L)** | L is the maximum word length (200). / L 為單字最大長度（200）。 |
| **Space** | **O(N × L)** | Storing the Trie nodes. / 儲存 Trie 節點。 |

---

## 6. Actionable Corrections (改進行動)

**English:**
1. **Memory Management:** Using `deque` with `maxlen` or manual popping ensures memory doesn't grow indefinitely ($O(L)$ instead of $O(\text{Total Queries})$).
2. **Reverse Insight:** The leap from "Suffix Search" to "Reversed Trie" is the most critical insight for this problem. It avoids the $O(N)$ check per query.

**中文：**
1. **記憶體管理：** 使用 `deque` 並限制長度，確保空間複雜度為 $O(L)$ 而不是隨查詢次數無限增長。
2. **反向思維：** 從「後綴搜尋」跳躍到「反向 Trie」是本題最關鍵的觀點，這有效避免了每次查詢都需要 $O(N)$ 的檢查。

---

## 7. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Reversed Trie** | A Trie storing reversed string sequences | 反向字典樹 |
| **Suffix Matching** | Checking if a pattern exists at the end of a string | 後綴匹配 |
| **Streaming Data** | Data that arrives continuously over time | 字元流 / 串流資料 |
| **Deque** | Double-ended queue, efficient for adding/removing at both ends | 雙端隊列 |
| **End of Word Marker** | A specific key (e.g., '#') to indicate a complete word | 單字結尾標記 |
