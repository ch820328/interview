# Advanced Graph: Shortest Path (進階圖論：最短路徑)

### 📌 核心概念
在帶有權重 (Weighted) 的圖中尋找點到點，或是單源到所有點的最短路徑。

### 📌 各種演算法比較與適用情境
- **Dijkstra's Algorithm**:
  - **適用**：單源最短路徑，且圖中**沒有負權重邊**。
  - **時間複雜度**：O((V + E) log V) (搭配 Min Heap)。
  - **核心**：貪心法 (Greedy)，每次從 Heap 中取出當前距離起點最近的節點進行 Relaxation (鬆弛)。
- **Bellman-Ford Algorithm**:
  - **適用**：單源最短路徑，圖中**允許有負權重邊**，且可用來偵測**負權重環 (Negative Weight Cycle)**。
  - **時間複雜度**：O(V * E)。
  - **核心**：對所有邊進行 V-1 次的 Relaxation。如果第 V 次還能 Relax，代表有負權重環。
- **A* Search Algorithm (A星演算法)**:
  - **適用**：單源單目標的最短路徑。在地圖導航、遊戲尋路中最常用。
  - **核心**：在 Dijkstra 的基礎上加入**啟發式函數 (Heuristic Function, e.g., 曼哈頓距離或歐幾里德距離)**。`f(n) = g(n) + h(n)`，`g(n)` 是起點到當前點的實際代價，`h(n)` 是當前點到終點的預估代價。
- **Floyd-Warshall Algorithm**:
  - **適用**：多源最短路徑 (找任意兩點之間的最短路徑)。
  - **時間複雜度**：O(V^3)，通常只適用於節點數很小 (V < 400) 的密集群。
  - **核心**：三維 DP (可壓縮為二維)，狀態轉移方程式為 `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j])`。

### 💻 經典模板與 Sample Code

#### 模板 1：Dijkstra's Algorithm (使用 Python `heapq`)
給定一個起點，求其到其他所有點的最短距離。
**Python**:
```python
import heapq

def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    # 建立 Adjacency List: graph[u] = [(v, weight), ...]
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
        # 若為無向圖需加上 graph[v].append((u, w))
        
    # min_heap 儲存 (目前累積距離, 當前節點)
    min_heap = [(0, start)]
    shortest_path = {} # node -> min_distance
    
    while min_heap:
        curr_dist, u = heapq.heappop(min_heap)
        
        # 由於同一個節點可能被以不同距離加入 Heap 多次，
        # 取出時若發現該節點已經被確定最短距離，則跳過 (Dijkstra 確保第一次彈出的就是最短)
        if u in shortest_path:
            continue
            
        shortest_path[u] = curr_dist
        
        for v, weight in graph[u]:
            if v not in shortest_path:
                heapq.heappush(min_heap, (curr_dist + weight, v))
                
    # 若有節點無法抵達，會沒出現在 shortest_path 中
    return shortest_path
```

#### 模板 2：A* Search Algorithm
在二維網格找點到點，假設代價都是 1。
**Python**:
```python
import heapq

def a_star(grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]) -> int:
    # 曼哈頓距離 heuristic 函數
    def heuristic(r, c):
        return abs(r - end[0]) + abs(c - end[1])
        
    rows, cols = len(grid), len(grid[0])
    # 儲存結構: (f_score, g_score, (r, c))
    min_heap = [(0 + heuristic(*start), 0, start)]
    visited = set()
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while min_heap:
        f, g, (r, c) = heapq.heappop(min_heap)
        
        if (r, c) == end:
            return g # 找到終點
            
        if (r, c) in visited:
            continue
        visited.add((r, c))
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                if (nr, nc) not in visited:
                    new_g = g + 1
                    new_h = heuristic(nr, nc)
                    heapq.heappush(min_heap, (new_g + new_h, new_g, (nr, nc)))
                    
    return -1 # 沒有路
```
