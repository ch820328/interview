# Advanced Graphs: Dependency & Connectivity (進階圖論：依賴與連通性)

## I. Problem Statement & Nuances (題目與細節)
How do we model systems with strict dependencies or determine if elements belong to the same cluster efficiently? These advanced graph techniques are the backbone of modern build systems and distributed networks.
我們如何為具有嚴格依賴關係的系統建模，或者有效率地判斷元素是否屬於同一個集群？這些進階圖論技術是現代構建系統與分散式網路的骨幹。

**Nucleus Insights (核心觀點):**
- **DAG (Directed Acyclic Graph)**: The natural structure for dependencies. If a graph has a cycle, there is no linear "valid" order. (DAG 是依賴關係的自然結構；若有環，則不存在線性順序。)
- **Union-Find (DSU)**: A specialized data structure that keeps track of elements split into several non-overlapping sets. (並查集是一種處理不相交集合合併與查詢的核心結構。)
- **Scaling Complexity**: Finding connectivity in a static graph is easy (DFS); doing it **dynamically** as edges are added requires DSU. (靜態連通性用 DFS，動態增加邊的連通性則需用並查集。)

---

## II. Mechanical Deep-Dive: The Mechanics of Dependencies (底層原理：依賴機制)

### 1. Topological Sort (Kahn's Algorithm)
Used for determining a linear order of tasks.
用於決定任務的線性順序。
- **Mechanism**: Count the **In-degree** (number of incoming edges) for each node.
- **Process**: Repeatedly remove nodes with 0 in-degree and add them to the queue. (重複移除入度為 0 的節點。)

### 2. Union-Find (Disjoint Set Union)
Used for cycle detection and connected components.
用於環偵測與連通分量。
- **Find**: Find the "Parent/Root" of an element. (尋找代表元素。)
- **Union**: Merge two sets by pointing one root to another. (合併兩個集合。)
- **Optimization**: **Path Compression** and **Union by Rank** make operations nearly $O(1)$ (Inverse Ackermann function $\alpha(N)$).

---

## III. Quantitative Analysis: Efficiency Trade-offs (量化指標分析)

| Algorithm | Best Use Case | Time Complexity | Note (備註) |
|---|---|---|---|
| **Topological Sort** | Build systems (Makefile). | $O(V + E)$ | Requires a DAG. |
| **Union-Find (DSU)** | Dynamic Connectivity. | $O(E \alpha(V))$ | Nearly constant time. |
| **Tarjan’s Algo** | Finding Clusters (SCC). | $O(V + E)$ | Finds strongly connected cycles. |

---

## IV. Infrastructure Ecosystem (基礎設施生態系)

| System | Algorithm | Why? (為什麼？) |
|---|---|---|
| **Terraform / Bazel** | **Topological Sort** | Resolving resource creation order based on dependencies. (解析資源創建順序。) |
| **Networking (Spanning Tree)** | **Union-Find** | Detecting cycles when bridges connect. (偵測網路環路。) |
| **Cluster Management** | Tarjan's / SCC | Identifying deadlocks in resource allocation graphs. (辨識資源分配圖中的死結。) |

---

## V. Code: Production Grade (Union-Find with Optimizations)

```go
package main

type DSU struct {
    parent []int
    rank   []int // Union by Rank optimization
}

func NewDSU(n int) *DSU {
    p := make([]int, n)
    r := make([]int, n)
    for i := range p {
        p[i] = i
    }
    return &DSU{parent: p, rank: r}
}

// Find: with Path Compression (專家級：路徑壓縮)
func (d *DSU) Find(i int) int {
    if d.parent[i] == i {
        return i
    }
    d.parent[i] = d.Find(d.parent[i]) // Recursive path compression
    return d.parent[i]
}

// Union: with Rank (專家級：按秩合併)
func (d *DSU) Union(i, j int) {
    rootI := d.Find(i)
    rootJ := d.Find(j)
    if rootI != rootJ {
        if d.rank[rootI] < d.rank[rootJ] {
            d.parent[rootI] = rootJ
        } else if d.rank[rootI] > d.rank[rootJ] {
            d.parent[rootJ] = rootI
        } else {
            d.parent[rootI] = rootJ
            d.rank[rootJ]++
        }
    }
}
```

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Cycles in Topo Sort**: If the sort produces an output shorter than the number of nodes, a **Cycle** exists. (若輸出長度不足，代表系統存在循環依賴。)
2. **DSU without Optimizations**: Without path compression, `Find` can degenerate to $O(N)$ (linked list). (若無路徑壓縮，並查集效能會大幅下降。)
3. **Directed vs Undirected**: Union-Find is primarily for **Undirected** graphs; for directed cycle detection, use DFS (Coloring) or Topo Sort. (並查集主要用於無向圖；有向圖判環請用 DFS 或拓撲排序。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| In-degree | 入度 | Number of edges directed towards a node. (指向該節點的邊的數量。) |
| DAG | 有向無環圖 | A directed graph with no cycles. (沒有迴圈的有向圖。) |
| Strongly Connected | 強連通 | A state where every node in a cluster is reachable from any other node. (集群中任兩點皆可互相到達。) |
| Path Compression | 路徑壓縮 | Optimization that flattens tree structure during Find. (在尋找根節點時將樹結構扁平化的優化。) |
