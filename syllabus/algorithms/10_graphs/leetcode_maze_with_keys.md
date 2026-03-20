# Coding Interview: Maze with Keys (迷宮與鑰匙 — 可達性分析)

**Topic / 主題:** State-Space Search / 狀態空間搜尋 (BFS)
**Difficulty / 難度:** Hard (LeetCode 864 variant)
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-10

---

## 1. Problem Statement (題目)

**English:**
Given a 2D grid maze containing empty spaces (`.`), walls (`#`), doors (`A-F`), keys (`a-f`), a start (`@`), and a target (`*`). 
To pass a door, you must have the corresponding key. Keys are not consumed. Determine if the target `*` is reachable from `@`.

**中文：**
給定一個 2D 網格迷宮，包含空地 (`.`)、牆壁 (`#`)、門 (`A-F`)、鑰匙 (`a-f`)、起點 (`@`) 與終點 (`*`)。
通過門需要對應的鑰匙，且鑰匙不會被消耗。請判斷從起點能否到達終點。

**Constraints / 限制條件:**
- Grid Size: 30x30
- Distinct Keys: Up to 6 (a-f)
- Reachability only (Shortest path not required / 僅需判斷可達性，不需最短路徑)

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Are keys consumed? / 鑰匙會被消耗嗎？ | No. / 不會。 |
| Reachability or Shortest Path? / 是判斷可達性還是求最短路徑？ | Reachability only. / 僅需可達性。 |
| Number of keys? / 鑰匙數量？ | Up to 6. / 最多 6 種。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **L5 Optimization: Greedy BFS** | Instead of a full $O(N \cdot 2^K)$ bitmask state, use $O(N)$ by tracking current keys and a "locked doors" map. / 不使用完整狀態空間，改用 $O(N)$ 策略：追蹤已獲取的鑰匙與「被鎖住的門」。 |
| **Locked Map Mechanism** | When a door is reached without its key, store its coordinates in `locked[required_key]`. / 當到達沒鑰匙的門時，將其座標存入 `locked[所需鑰匙]`。 |
| **Key Trigger** | Upon finding a key, immediately add all corresponding doors from the `locked` map back to the BFS queue. / 發現鑰匙時，立即將該鑰匙對應的所有「被鎖住的門」加入搜尋佇列。 |

**Why O(N) works for reachability? / 為什麼 O(N) 對可達性有效？**
In a shortest-path problem, we might need to revisit cells with different key sets. However, for **reachability**, once a cell is visited, revisiting it with more keys only adds value if it unlocks a door. By "teleporting" to unlocked doors directly via the map, we cover all new reachable areas in linear time.

在最短路徑問題中，我們需要帶位元遮罩的狀態空間。但對於**可達性**，重複造訪格子只有在「能開門」時才有意義。透過將「被鎖住的門」記錄下來並在拿到鑰匙後直接加入佇列，我們能以線性時間涵蓋所有新區域。

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
from typing import List
from collections import deque, defaultdict

class Solution:
    def canReachTarget(self, grid: List[str]) -> bool:
        if not grid or not grid[0]: return False
        
        rows, cols = len(grid), len(grid[0])
        start_node = None
        
        # 1. Initialize logic
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '@':
                    start_node = (r, c)
                    break
        
        if not start_node: return False
        
        queue = deque([start_node])
        visited = {start_node}
        keys = set()
        locked = defaultdict(set) # key -> set of door coordinates
        
        # 2. BFS Process
        while queue:
            curr_r, curr_c = queue.popleft()
            
            # Check neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = curr_r + dr, curr_c + dc
                
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                    char = grid[nr][nc]
                    
                    if char == '#': 
                        continue
                    
                    if char == '*':
                        return True
                    
                    # Door logic: wait if no key
                    if 'A' <= char <= 'F':
                        required_key = char.lower()
                        if required_key in keys:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                        else:
                            locked[required_key].add((nr, nc))
                    
                    # Key logic: pick up and unlock doors
                    elif 'a' <= char <= 'f':
                        keys.add(char)
                        visited.add((nr, nc))
                        queue.append((nr, nc))
                        if char in locked:
                            for door_coords in locked[char]:
                                if door_coords not in visited:
                                    visited.add(door_coords)
                                    queue.append(door_coords)
                            del locked[char]
                    
                    # Empty space
                    else:
                        visited.add((nr, nc))
                        queue.append((nr, nc))
                        
        return False

# --- Test harness (測試) ---
if __name__ == "__main__":
    sol = Solution()
    # Case 1: Simple Bypass
    grid1 = ["@.a.#", "###.#", "b.A.*"]
    print(sol.canReachTarget(grid1))  # True
    
    # Case 2: Locked behind walls
    grid2 = ["@...#", "#####", "a..A*"]
    print(sol.canReachTarget(grid2))  # False
    
    # Case 3: Key behind door (Sequence matter)
    grid3 = ["@.B.b", "####.", "a..A*"]
    # Path: @ -> A(locked) -> b -> B(open) -> a -> A(open) -> *
    print(sol.canReachTarget(grid3))  # True
```

---

## 5. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Time / 時間** | **O(R × C)** | Each cell is visited at most once. Keys/Doors add a constant factor of map lookups. / 每個格子最多造訪一次。 |
| **Space / 空間** | **O(R × C)** | Visited set and Locked map store up to the number of cells. / 集合與 Map 最多儲存所有格子的座標。 |

---

## 6. Common Bugs (常見錯誤)

| Bug (錯誤) | Root Cause (根本原因) | Fix (修正) |
|---|---|---|
| Forgetting to revisit doors | Reaching a door without a key then moving on | Use a `locked` map to store and re-add doors to queue later |
| 忘記回頭去開門 | 先到達門但沒鑰匙，之後拿到鑰匙卻沒去開門 | 使用 Map 儲存被鎖住的門，並在拿到鑰匙後加入佇列 |
| BFS as DFS | Using `pop()` instead of `popleft()` | Use `collections.deque` and `popleft()` |
| BFS 變 DFS | 誤用 `pop()` 從後方取出 | 使用 `popleft()` 確保階層遍歷 |

---

## 7. Actionable Corrections (改進行動)

**English:**
1. **Identify constraints to optimize:** Always ask "Is this reachability or shortest path?". An $O(N)$ solution is much more impressive to an L5 interviewer than a standard $O(N \cdot 2^K)$ one for simple connectivity.
2. **Atomic Queueing:** Add to `visited` at the moment of `append` to the queue, not at `pop`, to avoid duplicate entries in the queue.

**中文：**
1. **識別優化限制：** 永遠先問「是求路徑還是可達性？」。在可達性問題中，提出 $O(N)$ 解法比通用的 $O(N \cdot 2^K)$ 更能展現 L5 等級的洞察力。
2. **原子化佇列操作：** 在 `append` 進佇列的當下就標記 `visited`，而非在 `pop` 時才標記，可避免重複佇列導致的性能浪費。

---

## 8. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **State-Space Search** | Searching through all possible configurations of a system | 狀態空間搜尋 |
| **Bitmask** | Using bits of an integer to represent a set of boolean flags | 位元遮罩 |
| **Reachability** | Determining if a path exists between two nodes | 可達性分析 |
| **Greedy BFS** | An optimized BFS that doesn't track full state history | 貪婪式廣度優先搜尋 |
| **Locked Map** | A map used to store pending actions tied to a specific requirement | 鎖存地圖 (延遲任務清單) |
| **FIFO Queue** | First-In-First-Out data structure used in BFS | 先進先出佇列 |
