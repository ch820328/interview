# Google L4/L5 Coding Mock Interview — Koko Eating Bananas
# Google L4/L5 程式編碼模擬面試 — Koko 吃香蕉

**Interviewer:** Google Coding Interviewer (L5 Standard)
**Topic / 主題:** Binary Search on Answer | 值域二分搜尋
**Rating / 評級:** Hire

---

## 📝 Problem Statement | 題目

Given `n` piles of bananas and `h` hours, find the minimum integer eating speed `k` (bananas/hour) such that Koko can finish all piles within `h` hours. Each hour she picks one pile and eats `min(pile, k)` bananas.

給定 `n` 堆香蕉和 `h` 小時，找出最小整數吃速 `k`（香蕉／小時），使 Koko 能在 `h` 小時內吃完所有香蕉。每小時選一堆，吃 `min(pile, k)` 根。

```
Input:  piles=[3,6,7,11], h=8      → Output: 4
Input:  piles=[30,11,23,5,4], h=5  → Output: 30
```

**Constraints / 限制:**
- `1 <= piles.length <= 10^4`
- `piles.length <= h <= 10^9`
- `1 <= piles[i] <= 10^9`
- `k` must be a **positive integer** — no floats
- One pile per hour — even if `k > pile`, the hour is consumed

---

## 🔍 Clarification Phase | 釐清階段

| Question | Answer |
|---|---|
| Can speed `k` be a float? | ❌ No — must be positive integer |
| If `k > pile`, does it still take 1 hour? | ✅ Yes — one pile per hour regardless |
| Is `piles` guaranteed non-empty? | ✅ Yes |

---

## 💡 Approach | 解題思路

### Core Insight | 核心思想
The answer space `[1, max(piles)]` is **monotonically feasible**:
- If speed `k` works → any `k' > k` also works.
- This monotonicity enables **binary search on the answer**.

搜索空間 `[1, max(piles)]` 具有**單調可行性**：速度 `k` 可行 → 任何 `k' > k` 也可行。可對答案進行二分搜尋。

### Brute Force | 暴力法
- Try every speed from 1 to `max(piles)`.
- For each speed, compute total hours needed: O(N).
- **Time: O(max(piles) × N)** — too slow for `piles[i]` up to 10⁹.

### Optimal: Binary Search on Answer | 最優解：值域二分搜尋
- Binary search over `[1, max(piles)]`.
- Feasibility check: `sum(ceil(p/k) for p in piles) <= h`.
- **Time: O(N × log(max(piles)))** | **Space: O(1)**

### Ceiling Division Formula | 整數上取整公式
```python
ceil(p / k)  ==  ((p - 1) // k) + 1  ==  (p + k - 1) // k
```
Use `((p-1)//k)+1` to avoid importing `math`. 避免引入 math 模組。

---

## ✅ Final Clean Solution | 最終解答

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def get_hours_needed(speed: int) -> int:
            return sum(((p - 1) // speed + 1) for p in piles)

        l, r = 1, max(piles)

        while r > l:
            mid = (l + r) // 2
            if get_hours_needed(mid) <= h:
                r = mid          # mid is feasible → try smaller
            else:
                l = mid + 1      # mid not feasible → must go higher

        return r  # l == r at termination

if __name__ == "__main__":
    s = Solution()
    print(s.minEatingSpeed([3, 6, 7, 11], 8))       # 4
    print(s.minEatingSpeed([30, 11, 23, 5, 4], 5))  # 30
    print(s.minEatingSpeed([1_000_000_000], 1))      # 1_000_000_000
```

---

## 🧪 Dry Run | 手動追蹤

**Input:** `piles=[3,6,7,11], h=8`

| Round | l | r | mid | hours_needed | Feasible? | Action |
|---|---|---|---|---|---|---|
| 1 | 1 | 11 | 6 | 1+1+2+2=**6** | ✅ 6≤8 | r=6 |
| 2 | 1 | 6 | 3 | 1+2+3+4=**10** | ❌ 10>8 | l=4 |
| 3 | 4 | 6 | 5 | 1+2+2+3=**8** | ✅ 8≤8 | r=5 |
| 4 | 4 | 5 | 4 | 1+2+2+3=**8** | ✅ 8≤8 | r=4 |
| Exit | 4 | 4 | — | l==r → return **4** ✅ | | |

> ⚠️ **Common dry run error:** Round 2 hours = 10, not 9. Always compute each pile individually: `ceil(3/3)=1, ceil(6/3)=2, ceil(7/3)=3, ceil(11/3)=4 → sum=10`.

---

## 🐛 Common Bugs to Avoid | 常見錯誤

| Bug | Fix |
|---|---|
| `(p-1) / mid` — float division, missing `+1` | Use `((p-1) // mid) + 1` (integer ceiling) |
| `while l < r` with `r = mid - 1` — wrong template for minimum search | Use `while r > l` + `r = mid` + `l = mid + 1` |
| `-> bool` return type annotation | Return type is `-> int` |
| Missing `__main__` guard | Always add `if __name__ == "__main__":` |
| Not offering equivalent: `math.ceil(p/k)` | Proactively mention both forms and justify your choice |

---

## 🔑 Binary Search Template: Find Minimum Feasible | 二分搜尋模板：找最小可行值

```python
l, r = lower_bound, upper_bound

while r > l:
    mid = (l + r) // 2
    if is_feasible(mid):
        r = mid        # try smaller
    else:
        l = mid + 1    # must go higher

return r  # l == r: the minimum feasible value
```

**When to use:** Whenever the answer space is monotonic (feasible → all larger values also feasible). Classic examples: Koko Eating Bananas, Capacity to Ship Packages, Split Array Largest Sum.
**適用場景：** 答案空間具有單調性（可行 → 更大的值也可行）。經典題目：Koko 吃香蕉、裝貨最小載重、分割陣列最大值最小化。

---

## 📊 Final Evaluation | 最終評估

**Overall Rating / 總體評級:** `Hire`

| Dimension | Feedback |
|---|---|
| **Problem mapping** | ✅ Immediately identified binary search on answer with correct search space |
| **Feasibility formula** | ✅ Self-corrected bug from one hint — no answer given |
| **Binary search template** | ✅ Perfect minimum-feasible template, no off-by-one errors |
| **Helper function** | ✅ `get_hours_needed` — clean and self-documenting |
| **Dry run** | ✅ Structurally correct; minor arithmetic error in Round 2 (9 vs 10 — same conclusion) |
| **Type annotation** | ⚠️ `-> bool` instead of `-> int`; self-corrected after feedback |
| **`__main__` guard** | ⚠️ Not included despite being explicitly requested (3rd consecutive omission) |

### Actionable Corrections | 改善建議

1. **Slow down during dry runs.** 放慢 Dry Run 速度，逐一計算再加總，算術失誤損害可信度。
2. **`__main__` guard is non-negotiable.** 已連續三場面試遺漏，必須成為反射動作。
3. **Offer equivalent expressions proactively.** 主動說明 `((p-1)//k)+1` 等同於 `math.ceil(p/k)`，選前者以避免 import — 一句話展示深度。
