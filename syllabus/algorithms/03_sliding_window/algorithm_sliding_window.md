# Sliding Window (滑動視窗)

### 📌 核心概念
維持一個變動大小的「視窗」（通常是由 left 和 right 指針定義的區間），用來解決陣列或字串的「連續子陣列 / 子字串」問題。

### 📌 適用情境 (何時該想到它？)
- 題目要求尋找**連續**的子陣列或子字串（例如：最長、最短、包含某種字元的區間）。
- 問題的解具有「單調性」：當視窗擴張時，條件滿足程度逐漸增加（或減少）；縮小時則相反。

### 📌 優缺點分析 (Trade-offs)
- **優點**：能將巢狀迴圈遍歷所有子陣列的 O(N²) 時間優化為 O(N)。
- **缺點**：只能解決「連續」的片段問題，不能應付跳躍式或子序列 (Subsequence) 問題。

### 💻 經典模板與 Sample Code

#### 模板：動態視窗 (Longest Substring Without Repeating Characters)
標準的實戰積木套路：擴張 `right`，如果違規就移動 `left`。
**Python**:
```python
def lengthOfLongestSubstring(s: str) -> int:
    char_set = set()
    left = 0
    max_len = 0
    
    for right in range(len(s)):
        # 1. 遇到違規狀態，持續收縮 Left 直到合法
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
            
        # 2. 加入當前元素，並更新全局最大值
        char_set.add(s[right])
        max_len = max(max_len, right - left + 1)
        
    return max_len
```

---

## 🛑 L5 級別實戰注意：避免無謂的 O(K) 字串切片開銷
在 Python 等高階語言中，**字串切片 (`s[left:right]`) 是一個 $O(K)$ 的昂貴操作**（K 是切出來的字串長度）。
在滑動視窗不斷收放的 `while` 迴圈中，如果你為了紀錄目前的「最佳字串」，而不斷地在迴圈內部執行字串切片賦值（例如 `res = s[l:r+1]`），這會讓時間複雜度在面對巨型測資時，硬生生從 $O(N)$ 退化到近乎 $O(N^2)$，導致 **Time Limit Exceeded (TLE)**。

**🎯 L5 最佳實踐 (The L5 Fix)：**
**「只記錄指標與長度，最後再切那一刀」**
在迴圈中，我們只用 $O(1)$ 的代價去更新 `min_len` 和 `best_left`。直到整個視窗把字串掃描完畢，確定了最終的起點與長度，才做那「唯一一次」的最終字串切片。

---

## 🌟 經典實戰題拆解：Minimum Window Substring (Hard)

**題目：** 在字串 `s` 中，找出包含字串 `t` 所有字元的最短連續子字串。

**破局點 (The Trick)：條件計數法 (Need/Have Counter)**
遇到需要蒐集多種不同字元（且有數量要求）的滑動視窗題，標準解答框架就是使用一個整數 `need` 來記錄「還有幾種目標字元還沒收齊」。
1. **右指標擴展 (`r += 1`)**：每吃進一個字元，就紀錄。若某個所需字元的數量剛剛好達標，就 `need -= 1`。
2. **左指標收縮 (`l += 1`)**：當 `need == 0` 時（代表收集完了），開始向右移動左指標，試圖縮短這個字串的長度，直到某個所需字元被丟掉導致數量不夠 (`need += 1`)，我們才停下來，換回右指標繼續擴展。

### 終極效能安全版 Code (Python)
完美避開迴圈內字串切片的 $O(M^2)$ 陷阱。

```python
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t or len(s) < len(t):
            return ""
            
        cnt_t = Counter(t)
        need = len(cnt_t) # 有幾種「不同的」字元需要達標
        cur = Counter()
        
        l = 0
        # 紀錄最佳解的狀態 (取代直接存字串)
        min_len = float('inf')
        best_l = -1 
        
        for r in range(len(s)):
            char = s[r]
            cur[char] += 1
            
            # 當這個字元的數量「剛好」達到需求時，need 才 -1
            if cur[char] == cnt_t[char]:
                need -= 1
                
            # 當所需字元全部收齊時，開始嘗試收縮左視窗
            while need == 0:
                # 1. 更新全局最小長度 (O(1) 操作，絕不在這裡切字串 s[l:r+1])
                if r - l + 1 < min_len:
                    min_len = r - l + 1
                    best_l = l
                
                # 2. 準備把左邊字元丟掉
                left_char = s[l]
                cur[left_char] -= 1
                
                # 如果丟掉的是我們需要的字元，且數量跌破標準了，need += 1
                if cur[left_char] < cnt_t[left_char]:
                    need += 1
                    
                l += 1 # 左指標往內縮
                
        # 整個迴圈跑完，定生死，只做這唯一一次切片
        return "" if min_len == float('inf') else s[best_l : best_l + min_len]
```

**複雜度分析：**
- **時間複雜度：** $O(M) + O(N)$ (更精確地說是 $O(M)$，其中 M 是 $s$ 的長度，N 是 $t$ 的長度)。`l` 跟 `r` 最多只會把 $s$ 各走過一遍，內部全為 $O(1)$ 的字典加減操作。**沒有 $O(K)$ 的切片陷阱**。
- **空間複雜度：** $O(|Σ|)$ (常數級別)。最多只會依賴兩個 Hash Map (或 Counter) 來儲存字元頻率，由於英文字母數量有限（最多 52 個大小寫），空間複雜度極限為 $O(1)$。
