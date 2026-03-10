# Coding Interview: Random Point in Non-overlapping Rectangles (矩陣隨機取點)

**Topic / 主題:** Prefix Sum & Binary Search / 前綴和與二分搜尋
**Difficulty / 難度:** Medium (LeetCode 497)
**Target Level / 目標等級:** Google L4
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-10

---

## 1. Problem Statement (題目)

**English:**
Given a list of non-overlapping axis-aligned rectangles, implement a class to pick a random integer point within the area covered by these rectangles. Each integer point must have an equal probability of being picked.

**中文：**
給定一組不重疊且與軸對齊的矩陣，實作一個類別，從這些矩陣涵蓋的區域中隨機挑選一個整數點。每個整數點被選中的機率必須相等。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Inclusive of boundaries? / 包含邊界嗎？ | Yes, $x1 \le x \le x2$ and $y1 \le y \le y2$. / 是的。 |
| Memory constraints? / 空間限制？ | $O(N)$ where $N$ is number of rectangles. Avoid $O(\text{Area})$. / $O(N)$，$N$ 為矩陣數量。避免 $O(\text{面積})$ 的解法。 |
| Pick time complexity? / 抽取的時間複雜度？ | $O(\log N)$ is expected. / 預期為 $O(\log N)$。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Weighted Sampling** | Since each point has equal probability, the chance of picking a specific rectangle depends on the number of points it contains. / 由於每個點機率相等，選中某個矩陣的機率取決於它包含的點數。 |
| **Prefix Sum Array** | Compute the cumulative count of points across rectangles. This maps a linear range $[1, \text{TotalPoints}]$ to specific rectangles. / 計算矩陣點數的累積和。這將 $[1, \text{總點數}]$ 的線性範圍對應到特定矩陣。 |
| **Binary Search** | Use `bisect_left` to find which rectangle the random number falls into in $O(\log N)$. / 使用 `bisect_left` 以 $O(\log N)$ 找到隨機數落在哪個矩陣中。 |
| **Point Mapping** | Once a rectangle is selected, map the offset within the rectangle's range to 2D coordinates $(dx, dy)$ using modulo and division. / 選定矩陣後，使用餘數與除法將偏置值映射到 2D 座標。 |

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
import random
import bisect
from typing import List

class Solution:
    def __init__(self, rects: List[List[int]]):
        self.rects = rects
        self.prefix_sums = []
        total = 0
        for x1, y1, x2, y2 in rects:
            # Number of integer points is (width * height)
            num_points = (x2 - x1 + 1) * (y2 - y1 + 1)
            total += num_points
            self.prefix_sums.append(total)
        self.total_points = total

    def pick(self) -> List[int]:
        # Pick a random point index from 1 to total_points
        target = random.randint(1, self.total_points)
        
        # Find the rectangle index using binary search
        rect_idx = bisect.bisect_left(self.prefix_sums, target)
        
        # Get rectangle coordinates
        x1, y1, x2, y2 = self.rects[rect_idx]
        
        # Determine the offset within this specific rectangle
        prev_sum = self.prefix_sums[rect_idx - 1] if rect_idx > 0 else 0
        offset = target - prev_sum - 1
        
        # Map offset to 2D (relative dx, dy)
        width = x2 - x1 + 1
        dx = offset % width
        dy = offset // width
        
        return [x1 + dx, y1 + dy]
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Init Time** | **O(N)** | Iterating once through $N$ rectangles. / 遍歷 $N$ 個矩陣一次。 |
| **Pick Time** | **O(log N)** | Binary search on the prefix sum array. / 在前綴和陣列上進行二分搜尋。 |
| **Space** | **O(N)** | Storing the prefix sums and original rectangles. / 儲存前綴和與原始矩陣。 |

---

## 6. Actionable Corrections (改進行動)

**English:**
1. **Formula Check:** Always remember that the number of integer points between $x1$ and $x2$ is $(x2 - x1 + 1)$. Skipping the `+1` is a common L4/L5 bug.
2. **Modulo Logic:** Using `dy = offset // width` and `dx = offset % width` is an elegant way to map a 1D index to a 2D grid. It shows mathematical maturity.

**中文：**
1. **公式檢查：** 永遠記得 $x1$ 到 $x2$ 之間的整數點數量是 $(x2 - x1 + 1)$。漏掉 `+1` 是 L4/L5 常見的 Bug。
2. **取模邏輯：** 使用 `//` 與 `%` 來將 1D 索引映射到 2D 網格是很優雅的做法，能展現數學思維的成熟度。

---

## 7. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Prefix Sum** | A sequence of partial sums of a given sequence | 前綴和 |
| **Weighted Sampling** | Picking items with probability proportional to a weight | 加權隨機取樣 |
| **Binary Search** | Efficiently finding an item in a sorted list by halving | 二分搜尋 |
| **Inclusive Range** | A range that includes both endpoints | 閉區間 (包含邊界) |
| **Linear Mapping** | Transforming a 1D point to a 2D coordinate system | 線性映射 |
