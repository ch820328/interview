# Topological Sort (拓撲排序)

### 📌 核心概念
針對有向無環圖 (DAG)。將問題的依賴關係排序，保證排在前面的任務不會依賴後面的任務。

### 📌 適用情境 (何時該想到它？)
- 題目出現「先決條件 (Prerequisite)」、「依賴關係 (Dependency)」。
- CI/CD Pipeline 流程排程、軟體套件安裝順序。

### 💻 經典模板與 Sample Code

#### 模板：Kahn's Algorithm (Course Schedule 判斷是否有環)
維護 `in-degree`，藉由 BFS 每次移除入度為 0 的點。
**Python**:
```python
from collections import deque

def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    adj = {i: [] for i in range(numCourses)}
    in_degree = [0] * numCourses
    
    # [1, 0] 表示要修 1，必須先修 0 (0 -> 1)
    for crs, pre in prerequisites:
        adj[pre].append(crs)
        in_degree[crs] += 1
        
    # 把入度為 0 的放入隊列
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        curr = queue.popleft()
        count += 1
        for neighbor in adj[curr]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    return count == numCourses # 如果處理完所有節點，代表沒環
```
