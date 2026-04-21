# Graph Algorithms: Bellman-Ford & Distance Vector (圖論演算法：Bellman-Ford 與 距離向量)

## I. Problem Statement & Nuances (題目與細節)
Given a weighted directed graph, find the shortest path from a source to all other vertices. Handle cases where edge weights can be negative.
在一個權重有向圖中，找出從起點到所有其他頂點的最短路徑。需處理邊權重為負數的情況。

**Nucleus Insights (核心觀點):**
- **Dijkstra's Limitation**: Why it fails with negative weights (Greedy locally becomes wrong globally). (為什麼 Dijkstra 在負權重下失效：局部最優不再等於全域最優。)
- **Relaxation Principle**: The core mechanism of updating `dist[v] = min(dist[v], dist[u] + weight(u, v))`. (「鬆弛」原理：更新最短路徑的核心機制。)
- **Distributed Nature**: How **Distance Vector (DV)** protocols (like RIP) use this algorithm in networking without a global map. (距離向量協定如 RIP 如何在沒有全域圖的情況下使用此演算法。)

---

## II. Mechanical Deep-Dive: The Relaxation Process (底層原理：鬆弛過程)

Bellman-Ford works by relaxing all $E$ edges $V-1$ times.
Bellman-Ford 透過對所有 $E$ 條邊進行 $V-1$ 次鬆弛來運作。

1. **Iteration Count**: A shortest path in a graph with $V$ vertices can have at most $V-1$ edges. (擁有 $V$ 個頂點的圖中，最短路徑最多包含 $V-1$ 條邊。)
2. **Negative Cycle Detection**: On the $V$-th iteration, if any distance still decreases, a **Negative Cycle** exists, meaning a "shortest path" is undefined ($-\infty$). (在第 $V$ 次迭代中，若距離仍能減少，則存在**負環**，代表最短路徑無定義。)

---

## III. Quantitative Analysis Table (量化指標分析)

| Metric (指標) | Bellman-Ford | Dijkstra (Heap) | Floyd-Warshall |
|---|---|---|---|
| **Time Complexity** | $O(V \times E)$ | $O(E \log V)$ | $O(V^3)$ |
| **Space Complexity**| $O(V)$ | $O(V)$ | $O(V^2)$ |
| **Negative Weights**| **Supported** | Not Supported | Supported |
| **Best For** | Sparse Graphs w/ Neg Weights | Dense Graphs w/ Pos Weights | All-Pairs Shortest Path |

---

## IV. Ecosystem Comparison: Pathfinding Strategy (生態系橫向對比)

| Feature (特性) | Bellman-Ford (DV) | Dijkstra (Link-State) | Note (備註) |
|---|---|---|---|
| **Protocol Type** | Distance Vector (RIP) | Link State (OSPF) | DV 只看鄰居，LS 看整張圖。 |
| **Convergence Speed** | Slow (Count to Infinity) | Fast | BF 可能會發生無窮計數問題。 |
| **Memory Cost** | Low | High (Needs full topology) | BF 適合記憶體極受限的嵌入式設備。 |

---

## V. Code: Production Grade (生產級範例程式 - Go)

```go
package main

import (
    "fmt"
    "math"
)

type Edge struct {
    From, To, Weight int
}

func BellmanFord(vCount int, edges []Edge, src int) ([]int, error) {
    dist := make([]int, vCount)
    for i := range dist {
        dist[i] = math.MaxInt32
    }
    dist[src] = 0

    // V-1 iterations
    for i := 1; i < vCount; i++ {
        for _, edge := range edges {
            // Trace: Update if a shorter path is found
            if dist[edge.From] != math.MaxInt32 && dist[edge.From]+edge.Weight < dist[edge.To] {
                dist[edge.To] = dist[edge.From] + edge.Weight
            }
        }
    }

    // Step 5: Check for negative cycles (專家檢測：負環偵測)
    for _, edge := range edges {
        if dist[edge.From] != math.MaxInt32 && dist[edge.From]+edge.Weight < dist[edge.To] {
            return nil, fmt.Errorf("graph contains negative weight cycle")
        }
    }

    return dist, nil
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Count-to-Infinity Problem**: In networking (DV), if a link goes down, nodes might keep incrementing costs indefinitely unless a "MAX_HOP" (e.g., 16 in RIP) is defined. (在網路傳輸中，若鏈路中斷，節點可能無限增加成本，除非定義最大跳數。)
2. **Disconnected Components**: If some vertices are unreachable, their distance remains at $\infty$. (不可到達的頂點，其距離保持為無限大。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Relaxation | 鬆弛 | The process of finding a shorter path to a vertex through an edge. (透過某條邊為頂點尋找更短路徑的過程。) |
| Negative Cycle | 負環 | A cycle where the total sum of edge weights is negative. (邊權重總和小於零的環。) |
| Distributed Algorithm | 分散式演算法 | Algorithm that runs on multiple nodes without global control. (在多個節點上執行且無全域控制的演算法。) |
| RIP (Routing Information Protocol) | 路由資訊協定 | A classic distance-vector routing protocol. (經典的距離向量路由協定。) |
