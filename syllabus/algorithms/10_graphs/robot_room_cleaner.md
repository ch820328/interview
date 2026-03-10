# Coding Interview: Robot Room Cleaner (掃地機器人)

**Topic / 主題:** Graph Traversal (DFS) / 圖論遍歷 (深度優先搜尋)
**Difficulty / 難度:** Hard (LeetCode 489)
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-10

---

## 1. Problem Statement (題目)

**English:**
You are controlling a robot in an unknown, finite grid-based room. Walls exist at the boundaries and potentially inside. You don't know the robot's starting position or orientation. 
Design an algorithm to clean all reachable cells and return the robot to its starting position.

**中文:**
你在一個未知的、有限的網格房間中控制一個機器人。房間邊界和內部可能存在牆壁。你不知道機器人的起始位置或朝向。
設計一個演算法來清理所有可到達的格子，並在完成後讓機器人回到起始位置。

**API Provided / 提供的 API:**
- `move()`: Returns `True` if moved forward, `False` if hit a wall.
- `turnLeft(k)` / `turnRight(k)`: Rotates 90 degrees k times.
- `clean()`: Cleans the current cell.

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (答案) |
|---|---|
| Is the room finite? / 房間是有限的嗎？ | Yes, fully enclosed. / 是的，完全封閉。 |
| Is move distance fixed? / 移動距離固定嗎？ | One grid cell per call. / 每次呼叫移動一格。 |
| Initial orientation known? / 初始朝向已知嗎？ | No, must use relative coordinates. / 不知，必須使用相對座標。 |

---

## 3. Think Aloud & Strategy (思考過程與策略)

| Strategy (策略) | Description (描述) |
|---|---|
| **Relative Coordinates** | Define start as `(0,0)` and initial heading as "Up". Track visited cells in a set. / 定義起點為 `(0,0)`，初始朝向為「上」。用集合紀錄已造訪路徑。 |
| **DFS Traversal** | For each cell, try 4 clockwise directions. If unvisited and `move()` succeeds, recurse. / 在每一格嘗試四個順時針方向。若未造訪且 `move()` 成功，進入遞迴。 |
| **Physical Backtracking** | After recursion returns, manually move robot back to parent cell and restore orientation. / 遞迴返回後，手動讓機器人後退一格並還原朝向。 |

**Backtracking Logic (回溯邏輯):**
To return to the previous cell and maintain the same direction:
`turnRight(2)` -> `move()` -> `turnRight(2)`

---

## 4. Optimal Solution — Python (最佳解 — Python)

```python
class Solution:
    def cleanRoom(self, robot):
        """
        :type robot: Robot
        :rtype: None
        """
        # Direction vectors (Up, Right, Down, Left)
        # 位移向量 (0-上, 1-右, 2-下, 3-左)
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        self.visited = set()
        
        # Start DFS from relative (0, 0) and direction 0
        self.dfs(robot, 0, 0, 0)

    def go_back(self, robot):
        """
        Backtrack physically: move back and restore original orientation.
        實施物理回溯：後退一格並還原原始朝向。
        """
        robot.turnRight()
        robot.turnRight()
        robot.move()
        robot.turnRight()
        robot.turnRight()

    def dfs(self, robot, x, y, d):
        # 1. Clean current and mark as visited
        robot.clean()
        self.visited.add((x, y))

        # 2. Explore 4 directions clockwise
        for i in range(4):
            # Calculate absolute direction based on current facing d
            new_d = (d + i) % 4
            nx = x + self.directions[new_d][0]
            ny = y + self.directions[new_d][1]

            # Try to move if target is not visited
            if (nx, ny) not in self.visited and robot.move():
                self.dfs(robot, nx, ny, new_d)
                # Important: sync physical position after recursion ends
                self.go_back(robot)

            # Rotate robot to prepare for the next direction
            robot.turnRight()
```

---

## 5. Step-by-Step Dry Run (逐步追蹤)

**Scenario:** Small 2x1 room. Robot at (0,0) facing "Up". Wall at (0,1).
**情境：** 2x1 小房間。機器人在 (0,0) 朝上。牆在 (0,1)。

| Step | Action | State (Position, Direction) | Notes |
|---|---|---|---|
| 1 | `dfs(0,0,0)` | (0,0), D=0 | `clean()`, `visited={(0,0)}` |
| 2 | Try `i=0` (Up) | (0,0), D=0 | `nx,ny = (0,1)`. `move()` -> `False` |
| 3 | `robot.turnRight()`| (0,0), D=1 | Now facing Right |
| 4 | Try `i=1` (Right)| (0,0), D=1 | `nx,ny = (1,0)`. `move()` -> `True` |
| 5 | `dfs(1,0,1)` | (1,0), D=1 | `clean()`, `visited={(0,0), (1,0)}` |
| 6 | ... | ... | No more valid `move()`, returns to step 5 |
| 7 | `go_back()` | (0,0), D=1 | Robot returns to start, facing same way |

---

## 6. Complexity Analysis (複雜度分析)

| | Complexity | Justification (說明) |
|---|---|---|
| **Time / 時間** | **O(N)** | N is number of reachable cells. Each cell visited once, each edge checked twice. / N 為可達格子數。每格造訪一次，每邊檢查兩次。 |
| **Space / 空間** | **O(N)** | Visited set + Recursion depth (up to N in worst case corridor). / 造訪集合 + 遞迴深度（最差情況為通道型房間）。 |

---

## 7. Actionable Corrections (改進行動)

**English:**
1. **Explicitly mention Stack Depth:** When asked about space complexity, don't forget the call stack. For DFS on a grid, it can grow to O(N).
2. **Handle orientation precisely:** Remind yourself that `robot.turnRight()` in the loop changes the robot's state, while `new_d` tracks the logical direction. Keeping these synced is key.

**中文碼:**
1. **明確提及堆疊深度：** 被問到空間複雜度時，別忘了遞迴堆疊。在網格上的 DFS，深度最高可達 O(N)。
2. **精確處理朝向：** 注意迴圈中的 `robot.turnRight()` 會改變機器人實體狀態，而 `new_d` 則是紀錄邏輯方向。確保兩者同步是關鍵。

---

## 8. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **DFS** | Depth First Search - exploring as far as possible before backtracking | 深度優先搜尋 |
| **Backtracking** | Returning to a previous state to explore other paths | 回溯 |
| **Relative Coordinates** | Positioning based on starting point instead of absolute map | 相對座標 |
| **Hash Set** | Data structure for O(1) average lookup to track state | 哈希集合 |
| **Offset Vector** | Predetermined coordinate shifts for movement (e.g., (0,1)) | 位移向量 |
| **State Synchronization** | Ensuring logical variables match physical robot position | 狀態同步 |
