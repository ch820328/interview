# Graph Theory & Traversal (圖論與遍歷)

### 📌 核心概念
由節點 (Vertices) 與邊 (Edges) 組成，可能會有向、無向、有權重或帶環 (Cycle)。遍歷圖的核心是 **DFS** 與 **BFS**。

### 📌 適用情境 (何時該想到它？)
- 題目描述地圖、網格、社群網路、相依性物件、迷宮。
- 尋找兩點之間的最短路徑（無權重圖 => BFS）。
- 尋找連通區塊 (Connected Components)。

### 📌 核心技巧：DFS vs BFS
- **DFS (深度優先搜尋)**：用 Stack 或遞迴實作。找連通塊、狀態組合。
  - **必留心眼**：必須維護 `visited` 集合，否則會陷入死迴圈。
- **BFS (廣度優先搜尋)**：用 Queue 實作。用於無權重圖的「最短路徑」或「層級擴散」。

### 💻 經典模板與 Sample Code

#### 模板：網格中的 DFS (Number of Islands)
用來尋找連通區塊，碰到陸地 (`1`) 就開始 DFS 把相連的陸地沉沒 (`0`)。
**Python**:
```python
def numIslands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        # 越界或是遇到海水(0)、已經沉沒的陸地(0)
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
            return
        # 把陸地變為海水以標記為已拜訪
        grid[r][c] = '0'
        # 往四個方向搜索
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count
```

#### 模板：無權重圖最短路徑 (BFS)
**Python**:
```python
from collections import deque

def minJumps(edges: dict[int, list[int]], start: int, target: int) -> int:
    queue = deque([start])
    visited = set([start])
    steps = 0
    
    while queue:
        size = len(queue)
        for _ in range(size):
            curr = queue.popleft()
            
            if curr == target:
                return steps
                
            for neighbor in edges.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        steps += 1 # 每擴展一層，步數 +1
        
    return -1 # 無法到達
```
