# Google L4/L5 Coding Mock Interview — Course Schedule
# Google L4/L5 程式編碼模擬面試 — 課程排程

**Interviewer:** Google Coding Interviewer (L5 Standard)
**Topic / 主題:** Graph BFS / Topological Sort (Kahn's Algorithm) | 圖論 BFS / 拓撲排序（卡恩演算法）
**Rating / 評級:** Hire

---

## 📝 Problem Statement | 題目

Given `numCourses` courses labeled `0` to `numCourses - 1`, and `prerequisites[i] = [a, b]` meaning you must take course `b` before `a`, return `true` if you can finish all courses.

給定 `numCourses` 門課程（編號 0 到 numCourses-1），`prerequisites[i] = [a, b]` 代表修 a 前必須先修 b。若所有課程可完成則回傳 `true`。

```
Input:  numCourses=2, prerequisites=[[1,0]]        → Output: true
Input:  numCourses=2, prerequisites=[[1,0],[0,1]]  → Output: false  ← cycle
```

**Constraints / 限制:**
- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- All pairs `[a, b]` are unique; no self-loops
- 所有配對唯一；無自環

---

## 🔍 Clarification Phase | 釐清階段

| Question | Answer |
|---|---|
| `numCourses = 2` means courses 0 and 1? | ✅ Yes — courses labeled 0 to N-1 |
| If no prerequisites, can we always finish? | ✅ Yes — empty array → always `true` |
| Can prerequisites have duplicates or self-loops? | ❌ No — all pairs unique, no self-loops (per constraints) |

---

## 💡 Approach | 解題思路

### Core Insight | 核心思想
This is **Cycle Detection in a Directed Graph**.
這是**有向圖中的環偵測**問題。
- Each course = a node. Each prerequisite `[a, b]` = directed edge `b → a`.
- If the graph has a cycle → impossible to complete → return `false`.

### Brute Force | 暴力法
- DFS from **every** node; check if it can reach itself.
- O(V × (V+E)) — repeated traversal from each node.
- 對每個節點做 DFS 檢查是否能回到自身，重複計算。

### Optimal: Kahn's Algorithm (BFS Topological Sort) | 最優解：卡恩演算法

**Intuition / 直覺：**
- Count **in-degrees** (number of prerequisites) for each course.
- Courses with in-degree 0 can be taken immediately → enqueue them.
- Process each course: decrement neighbors' in-degree; if any hits 0, enqueue.
- If after exhausting the queue, all in-degrees are 0 → no cycle → `true`.

**Complexity / 複雜度:**
- Time: **O(V + E)** — each node and edge processed once
- Space: **O(V)** — in-degree array + queue + graph adjacency

---

## ✅ Final Clean Solution | 最終解答

```python
import collections

class Solution:
    def canFinish(self, numCourses: int, prerequisites: list[list[int]]) -> bool:
        in_degree = [0] * numCourses
        graph = collections.defaultdict(list)

        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        queue = collections.deque(
            course for course in range(numCourses) if in_degree[course] == 0
        )

        while queue:
            current = queue.popleft()
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return all(count == 0 for count in in_degree)

if __name__ == "__main__":
    s = Solution()
    print(s.canFinish(2, [[1, 0]]))              # True
    print(s.canFinish(2, [[1, 0], [0, 1]]))      # False
    print(s.canFinish(4, [[1,0],[2,0],[3,1],[3,2]]))  # True
```

---

## 🧪 Dry Run | 手動追蹤

**Input:** `numCourses=4, prerequisites=[[1,0],[2,0],[3,1],[3,2]]`
**Expected output:** `True` — DAG, no cycle. Course order: 0 → 1 → 2 → 3

```
graph     = {0: [1, 2], 1: [3], 2: [3]}
in_degree = [0, 1, 1, 2]
```

| Step | Pop | Action | in_degree after | Queue |
|---|---|---|---|---|
| Init | — | in_degree[0]=0 → enqueue | `[0,1,1,2]` | `[0]` |
| 1 | `0` | decrement 1,2 → both hit 0 | `[0,0,0,2]` | `[1,2]` |
| 2 | `1` | decrement 3 → in_degree[3]=1 | `[0,0,0,1]` | `[2]` |
| 3 | `2` | decrement 3 → in_degree[3]=0, enqueue | `[0,0,0,0]` | `[3]` |
| 4 | `3` | no neighbors | `[0,0,0,0]` | `[]` |
| **Return** | | `all(cnt==0)` → **True** ✅ | | |

---

## 🐛 Code Quality Notes | 程式碼品質提醒

| Issue (Candidate's Submission) | Correct Version |
|---|---|
| `pre` — ambiguous variable name | Use `in_degree` — self-documenting |
| `learnCourse` — non-canonical method name | Use `canFinish` — matches LeetCode/convention |
| `defaultdict(set)` — prevents duplicate edges | `defaultdict(list)` is sufficient (constraints guarantee no duplicates) |
| No `__main__` guard | Add `if __name__ == "__main__":` |

---

## 📊 Final Evaluation | 最終評估

**Overall Rating / 總體評級:** `Hire`

| Dimension | Feedback |
|---|---|
| **Clarification** | ✅ Clean targeted questions; confirmed edge cases upfront |
| **Problem Mapping** | ✅ Immediately identified Cycle Detection in Directed Graph — correct abstraction |
| **Brute Force** | ✅ O(V×(V+E)) correctly articulated |
| **Optimal Algorithm** | ✅ Named Kahn's Algorithm unprompted with correct complexity O(V+E) |
| **Implementation** | ✅ Correct on first serious submission — logic is sound |
| **Dry Run** | ✅ Flawless — every queue state and in_degree transition accurate |
| **Variable naming** | ⚠️ `pre` instead of `in_degree`; `learnCourse` instead of `canFinish` |

### Actionable Corrections | 改善建議

**English:**
1. **Use canonical, self-documenting names.** `in_degree` is universally understood in graph problems. `pre` forces every reader to infer meaning from context. In interviews and PRs, naming clarity signals engineering maturity.
2. **Follow domain naming conventions.** When a problem has a well-known name (`canFinish`), use it. Non-standard names create unnecessary cognitive load for reviewers.
3. **Your Think-Aloud was concise but correct.** For L5, add one more layer: proactively mention the alternative approach (DFS with 3-color visited states) and explain *why* you chose Kahn's over it (iterative, no recursion stack risk, cleaner termination condition).

**中文翻譯：**
1. **使用標準、自我說明的變數名稱。** `in_degree` 在圖論問題中是通用術語。`pre` 強迫讀者從上下文推斷含義。命名清晰度在面試與 PR 中都代表工程師的成熟度。
2. **遵循領域命名慣例。** 當問題有廣為人知的名稱（`canFinish`）時，直接使用。非標準名稱為審閱者增加不必要的認知負擔。
3. **Think-Aloud 簡潔但正確。** 若要達到 L5，再加一層：主動提及替代方案（DFS 三色標記法），並說明為何選擇 Kahn's（迭代式、無遞迴堆疊風險、終止條件更清楚）。

---

## 🔑 Key Concept: Kahn's vs DFS for Cycle Detection | 關鍵概念對比

| | Kahn's Algorithm (BFS) | DFS 3-Color |
|---|---|---|
| **Approach** | Process in-degree 0 nodes iteratively | Mark nodes: unvisited / visiting / visited |
| **Cycle detection** | Unprocessed nodes remain (in_degree > 0) | Back-edge found (visiting → visiting) |
| **Stack overflow risk** | ❌ None — iterative | ⚠️ Yes — deep recursion on large graphs |
| **Produces topo order** | ✅ Yes — order of processing | ✅ Yes — reverse postorder |
| **L5 preference** | ✅ Preferred for production | Acceptable but requires careful visited state |
