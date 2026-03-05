# Binary Search (二分搜尋)

### 📌 核心概念
在**有序**的搜尋空間中，每次透過判斷中點，將搜尋範圍砍半 (O(logN))。

### 📌 L4 級別實戰注意：邊界管理的藝術
二分搜是面試中最容易出 Bug 的演算法。必須熟悉一套死模板，否則非常容易寫出死迴圈（Infinite Loop）。在「對結果二分搜」的場合 (例如 Koko Eating Bananas)，更是極度考驗這個模板的掌握度。

### 💻 經典模板與 Sample Code (三種變形)

#### 模板 1：精確尋找 (標準 `left <= right`)
適用於陣列中只有一個元素符合條件，找到就直接回傳。
**Python**:
```python
def binarySearch(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    # 重點：left <= right，因為搜尋區間是 [left, right] 雙閉區間
    while left <= right:
        mid = left + (right - left) // 2 # 防止 Overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1 # Target 在右半邊
        else:
            right = mid - 1 # Target 在左半邊
    return -1
```

#### 模板 2：尋找左側邊界 (`left < right`)
適用於陣列中有重複元素，要求回傳第一個大於等於 target 的位置 (也就是 `lower_bound`)。
**Python**:
```python
def searchInsertPath(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    # 重點：left < right，搜尋區間是 [left, right) 左閉右開
    while left < right:
        mid = left + (right - left) // 2
        # 如果 mid 小於 target，代表 target 絕對不在 mid 及其左側
        if nums[mid] < target:
            left = mid + 1
        else:
            # nums[mid] >= target，mid 可能是答案，所以保留 mid (不能 mid - 1)
            right = mid 
            
    # 迴圈結束時 left == right，即為插入點或左邊界
    return left
```

#### 模板 3：尋找右側邊界 (`left < right` 且向上取整)
適用於尋找最後一個符合條件的元素。
**Python**:
```python
def searchRightBound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    # 搜尋區間 [left, right]
    while left < right:
        # 重點：找右邊界時，mid 必須向右 / 向上取整 + 1
        # 否則只剩下兩個元素時 (例如 [2, 2])，mid 永遠不動，導致死迴圈
        mid = left + (right - left + 1) // 2 
        
        if nums[mid] > target:
            right = mid - 1
        else:
            # nums[mid] <= target，mid 可能是答案，保留 mid
            left = mid
    # 需額外判斷是否存在
    return left if nums[left] == target else -1
```

---

## 🛑 進階剖析：邊界條件與 `mid` 的加減抉擇

面試時最常卡住的問題就是：「我到底要用 `while l <= r` 還是 `while l < r`？我的縮圈要寫 `l = mid + 1` 還是 `l = mid`？」
這完全取決於你的**搜尋區間定義**以及**你是否還要保留 `mid` 這個嫌疑犯**。

### 1. 迴圈條件的差異 (`l <= r` vs `l < r`)
*   **`while l <= r` (雙閉區間 `[l, r]`)**
    *   **意義**：當 `l == r` 也就是只剩下最後一個數字時，這個數字**還要被檢查一次**。迴圈終止條件是 `l > r` (通常是 `l = r + 1`)。
    *   **使用時機**：適用於「找尋唯一確定的目標」。找到了就 `return mid`，找不到等迴圈自然跳出後 `return -1`。
*   **`while l < r` (左閉右開區間 `[l, r)` 或收縮型)**
    *   **意義**：當 `l == r` 也就是只剩下最後一個數字時，代表**已經逼近出唯一解答**，不需要再檢查，直接跳出迴圈，回傳留在原地的 `l`（在某些例外寫法中也可以用 `l == r` 退出來做最後一次檢查）。
    *   **使用時機**：適用於「尋找邊界 (Lower Bound / Upper Bound)」或「找最小值/最大值」，不確定目標就是 `mid` 的場合。

### 2. 邊界收縮的差異 (`mid + 1`, `mid - 1` vs `mid`)
*   **什麼時候 +1 / -1？**
    如果你的 `if` 判斷式讓你**百分之百確定 `mid` 不會是答案**（例如 `nums[mid] < target`，那 `mid` 本身絕不可能是 target），請果斷使用 `l = mid + 1` 或是 `r = mid - 1` 把 `mid` 踢出嫌疑犯名單。
*   **什麼時候保留 `mid`？**
    如果你的 `if` 判斷式只代表「答案『可能』是 `mid` 或是落在 `mid` 旁邊」（例如 `nums[mid] >= target`，在找左邊界時，`mid` 有可能就是最左邊那個，也可能還有更左邊的），此時**絕對不能丟掉 `mid`**，必須寫成 `r = mid` 或 `l = mid`。

🔥 **極致死迴圈陷阱：**
如果你使用 `while l < r`，且出現了 `l = mid` 的收縮。當區間只剩下兩個元素 `[2, 3]` (例如 `l=0, r=1`) 時，`mid = (0+1)//2 = 0`。如果剛好又跑到 `l = mid`，那你的 `l` 還是 0，區間還是 `[0, 1]`，**永遠跑不出來**！
**解法**：在計算 `mid` 時向上取整：`mid = (l + r + 1) // 2`。

---

## 🌟 經典實戰題拆解：Search in Rotated Sorted Array

**題目：** 在一個原本遞增但被旋轉過（被截斷）的陣列中，尋找目標 `target`，要求 $O(\log N)$。

**難點：** 陣列並非單調遞增，無法直接無腦進行二分搜。
**破局點：** 只要隨便拿一刀 (mid) 切下去，**「左半邊」或「右半邊」必定有一邊是完全有序 (Strictly Sorted) 的。**

### 分析思維：
1. 先判斷哪一邊是有序區間？
   * 比較最左端與中點：如果 `nums[left] <= nums[mid]`，代表從 `left` 到 `mid` 是一條完美的上升坡道，**左半邊有序**。
   * 否則，必然是**右半邊有序** (`nums[mid] < nums[right]`)。
2. 檢查 `target` 是否「乖乖待在有序的坡道區間內」？
   * 如果是左半邊有序，且 `nums[left] <= target <= nums[mid]`：代表 target 就在這段坡道上，放心把視線鎖死在這，執行 `right = mid` 或 `right = mid - 1`。
   * 反之，即便左邊有序，但 `target` 不在坡道範圍內，那它必定在另一半的混亂區間，執行 `left = mid + 1` 往另一邊找。

### 終極安全解法碼 (Python)：
採用**逼近法 `while l < r`**，最後剩下一個元素時再做最後審問，完美避開死迴圈或邊界爆炸的問題。

```python
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l, r = 0, len(nums) - 1
        
        while l < r:
            mid = l + (r - l) // 2 # 防止 overflow 的 Pythonic 寫法
            
            # 左半邊是有序的
            if nums[l] <= nums[mid]:
                # target 乖乖落在左半邊的有序區間內
                if nums[l] <= target <= nums[mid]:
                    r = mid
                else:
                    l = mid + 1
            # 右半邊是有序的
            else:
                # target 乖乖落在右半邊的有序區間內
                if nums[mid] <= target <= nums[r]:
                    l = mid
                else:
                    r = mid - 1
                    
        # 迴圈終止時 l == r，剩下的這個數字才是最後嫌犯，需做驗證
        return l if nums[l] == target else -1
```

**複雜度分析：**
- **時間複雜度：** $O(\log N)$。每次判斷都會篩掉一半的數組。
- **空間複雜度：** $O(1)$。只使用了常數等級的指標變數 (`l`, `r`, `mid`)。

