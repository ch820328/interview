# Algorithm Deep Dive: Binary Search on Answer (對答案進行二分搜尋)

**Target Level:** Google L4 / L5 (Senior Software Engineer)
**Focus Area:** Binary Search Boundaries, Integer Arithmetic (Ceiling), Constraints Awareness, Code Coachability

---

## 📝 The Problem: Koko Eating Bananas

Koko loves to eat bananas. There are `n` piles of bananas, the `i`-th pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.
Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.
Return the **minimum integer `k`** such that she can eat all the bananas within `h` hours.

**Constraints:**
* `1 <= piles.length <= 10^4`
* `piles.length <= h <= 10^9`
* `1 <= piles[i] <= 10^9`

---

## 🧠 L5 Algorithm Breakdown

### 1. Identifying "Binary Search on Answer"
When a problem asks for the "minimum/maximum value that satisfies a condition," and the condition has a monotonic property (e.g., if speed $k$ works, speed $k+1$ definitely works; if speed $k$ fails, speed $k-1$ definitely fails), it perfectly points to Binary Search on the Answer Space.

### 2. Defining the Search Space
- **Lower Bound (`l = 1`):** The minimum possible eating speed is 1 banana per hour. (Speed cannot be 0).
- **Upper Bound (`r = max(piles)`):** The maximum eating speed we would ever need to consider. Since Koko can only eat from *one* pile per hour, even if her eating speed was infinity, eating a pile of size `max(piles)` still takes exactly 1 hour. The speed is effectively capped at the largest pile.

### 3. The L5 Trap: Redundant Constraint Checks & Over-Engineering
A common novice mistake is adding a sanity check like:
```python
if count(r, piles) > h: return -1
```
**Why this fails an L5 Interview:** Look at the constraints: `piles.length <= h`. 
If Koko eats at the maximum speed (`r = max(piles)`), every single pile takes exactly 1 hour. Therefore, the total time will be exactly `piles.length`. Since the constraint explicitly guarantees `piles.length <= h`, eating at the maximum speed implies it is mathematically impossible to exceed `h`. 

Writing defensive code for an impossible scenario shows an inability to fully digest and trust the system's provided constraints. It's redundant, wasteful code.

### 4. The L5 Math Trick: Integer Ceiling (整數無條件進位公式)
When Koko eats a pile of size `p` at speed `s`, the hours taken is the ceiling of `p / s`.
- **Novice Approach:** `math.ceil(p / s)` -> Introduces floating-point inaccuracies at massive scales and function call overhead.
- **Clever but Non-Standard Python Approach:** `p // s + int((p % s) > 0)` -> Works, but explicitly relies on casting booleans to integers.
- **The L5 Standard Execution (Zero Casts, Zero Floats):**
```python
hours = (p + s - 1) // s
```
*Why this works mathematically:* Adding `s - 1` ensures that if there is even *one* remainder element in the division, the numerator is pushed over the threshold to increment the floor division result by exactly `1`. If there is no remainder, adding `s - 1` isn't enough to cross into the next multiple of `s`. This is standard practice in stringent typed languages like C++ and Java.

---

## 💻 The Ultimate L5 Code Template

```python
class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        
        # Helper function acting as our condition verifier
        def can_finish(speed: int) -> bool:
            # L5 Math Trick: (p + speed - 1) // speed
            total_hours = sum((p + speed - 1) // speed for p in piles)
            return total_hours <= h

        # Define the exact Search Space
        l = 1
        r = max(piles)
        
        # Lower Bound Binary Search Template
        while l < r:
            mid = (l + r) // 2
            
            # If we CAN finish, this speed might be the minimum, 
            # or there might be an even smaller one. So keep 'mid' in the search space.
            if can_finish(mid):
                r = mid
            # If we CANNOT finish, this speed is strictly too slow.
            # We must search strictly faster speeds.
            else:
                l = mid + 1
                
        return l
```

### 📉 Complexity Analysis
* **Time Complexity:** $O(N \log(\max(P)))$ where $N$ is the number of piles and $P$ is the max number of bananas in a pile. We perform binary search over $O(\log(\max(P)))$ values, and for each value, we iterate through the $N$ piles array once.
* **Space Complexity:** $O(1)$. We only use a few integer variables (`l`, `r`, `mid`), requiring constant extra space.
