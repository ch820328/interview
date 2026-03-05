# Union-Find (並查集 / Disjoint Set)

### 📌 核心概念
用來快速判斷兩個元素是否屬於同一個集合，或將兩個集合合併。

### 📌 適用情境 (何時該想到它？)
- 處理「動態連通性 (Dynamic Connectivity)」問題。
- 尋找無向圖中是否有環。
- Kruskal 最小生成樹 (MST) 演算法的核心。

### 📌 核心技巧與 Trade-offs
必須加入 **Path Compression (路徑壓縮)** 與 **Union by Rank / Size** 優化。

### 💻 經典模板與 Sample Code

#### 模板：路徑壓縮 + 按規模合併 (Rank Optimization)
**Python**:
```python
class UnionFind:
    def __init__(self, size: int):
        self.root = [i for i in range(size)]
        self.rank = [1] * size

    def find(self, x: int) -> int:
        if x == self.root[x]:
            return x
        # Path Compression: 把每個節點都直接指向 root
        self.root[x] = self.find(self.root[x])
        return self.root[x]

    def union(self, x: int, y: int) -> bool:
        rootX = self.find(x)
        rootY = self.find(y)
        
        if rootX != rootY:
            # Union by Rank: 小樹接在大樹下
            if self.rank[rootX] > self.rank[rootY]:
                self.root[rootY] = rootX
            elif self.rank[rootX] < self.rank[rootY]:
                self.root[rootX] = rootY
            else:
                self.root[rootY] = rootX
                self.rank[rootX] += 1
            return True
        return False # 代表 x 與 y 本來就是同一個 Group (發現圖裡有環！)
```
