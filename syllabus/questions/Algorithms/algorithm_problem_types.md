# Algorithm Problem Types: The Interview Map (演算法題型總覽：面試全地圖)

## I. Overview & Nuances (概述與細節)
To master technical interviews, don't just memorize solutions; recognize **Patterns**. This map categorizes the most common algorithmic strategies used in top-tier companies.
要精通技術面試，不要只背程式碼，要學會辨識**模式 (Patterns)**。這份地圖分類了頂尖公司最常用的演算法策略。

**Nucleus Insights (核心觀點):**
- **Decision Trees**: Every problem is essentially a decision tree. (每個問題在本質上都是決策樹。)
- **Trade-offs**: Knowing when to switch from DFS to BFS, or Recursion to Iteration. (知道何時從 DFS 切換到 BFS，或從遞迴切換到迭代。)
- **Space-Time Duality**: Often, we spend memory (HashMaps) to buy time ($O(1)$ access). (通常我們用記憶體換取時間效率。)

---

## II. The Core Algorithmic Pillars (核心演算法支柱)

| Category (分類) | Common Patterns (常用模式) | Key Data Structures (關鍵資料結構) |
|---|---|---|
| **Arrays & Hashing** | Sliding Window, Two Pointers. | Hash Map, Multi-set. |
| **Two Pointers** | Fast & Slow (Rabbit & Turtle). | Linked List, Array. |
| **Sliding Window** | Fixed/Variable size. | Deque, Map. |
| **Stack & Queue** | Monotonic Stack. | Queue, Deque, Stack. |
| **Trees & Graphs** | DFS, BFS, Topo Sort, Union Find. | Adjacency List, Trie, Heap. |
| **Dynamic Programming** | Knapsack, LIS, LCS. | 2D Array, State Compression. |

---

## III. Quantitative Decision Table (量化決策表)

| Complexity Target | Likely Strategy (可能策略) | Note (備註) |
|---|---|---|
| $O(1)$ | Math, Bit Manupulation. | No iteration allowed. |
| $O(\log N)$ | Binary Search. | Sorted data or monotonic properties. |
| $O(N)$ | Two Pointers, Sliding Window, Hashing, Stack. | Linearly parsing data. |
| $O(N \log N)$ | Sorting, Heap, Divide & Conquer. | Sorting overhead. |
| $O(N^2)$ | Nested loops, simple DP. | Small $N$ (e.g., $N < 5000$). |
| $O(2^N)$ | Backtracking, Recursion (Brute Force). | Very small $N$ (e.g., $N < 20$). |

---

## IV. Graph Algorithm Ecosystem (圖論演算法生態系)

| Problem Type (問題類型) | Algorithms (演算法) | Complexity (複雜度) |
|---|---|---|
| **Shortest Path (Pos Weights)** | Dijkstra | $O(E \log V)$ |
| **Shortest Path (Neg Weights)** | **Bellman-Ford / SPFA** | $O(VE)$ |
| **All-Pairs Shortest Path** | Floyd-Warshall | $O(V^3)$ |
| **Minimum Spanning Tree** | Kruskal's / Prim's | $O(E \log E)$ |
| **Cycle Detection** | DFS / Union Find / Kahn's | $O(V+E)$ |

---

## V. Mastery Strategy: The "Blind" 75+ (精進策略：Blind 75+)
1. **Identify the Pattern First**: Read the problem, determine if it's "Sliding Window" or "DP".
2. **Handle Edge Cases**: Empty input, $N=1$, duplicate values.
3. **Analyze Complexity**: Always state $O(N)$ and $S(N)$ before writing code.

---

## VI. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Monotonic Stack | 單調棧 | A stack where elements are always in sorted order. (元素始終保持排序順序的堆疊。) |
| State Compression | 狀態壓縮 | Using bitmasks to represent DP states. (使用位元遮罩來代表動態規劃狀態。) |
| Amortized Analysis | 攤還分析 | Averaging the total cost of operations over time. (將操作總成本平攤到時間上的分析方法。) |
| Memoization | 記憶化 | Storing results of expensive function calls (Top-Down DP). (儲存昂貴函式呼叫結果的方法。) |
