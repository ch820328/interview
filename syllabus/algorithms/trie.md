# Trie (字典樹 / 前綴樹)

### 📌 核心概念
用來儲存字串的樹狀結構，每個節點代表一個字元，從根節點到任意節點的路徑代表一個前綴 (Prefix)。

### 📌 適用情境 (何時該想到它？)
- 處理大量字串，且經常需要搜尋字串是否有某個**前綴 (Prefix)**。
- 實作搜尋引擎的 Autocomplete (自動補全) 系統 (System Design 也很常考)。

### 💻 經典模板與 Sample Code

#### 模板：實作 Trie 的 Insert 與 Search
**Python**:
```python
class TrieNode:
    def __init__(self):
        self.children = {} # char -> TrieNode
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
```
