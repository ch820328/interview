# Binary Tree & BST (二元樹與二元搜尋樹)

### 📌 核心概念
- **Tree**: 由節點組成，每個結構有 0 到多個子節點，且不包含環。
- **BST (二元搜尋樹)**: 左子樹的所有節點值 < 根節點值 < 右子樹的所有節點值。

### 📌 適用情境 (何時該想到它？)
- 題目提到層級架構（如公司組織圖、檔案系統）。
- 題目出現 `Node`, `left`, `right` 等關鍵字。
- 需要以 O(logN) 的時間複雜度進行尋找、插入、刪除（如果是一棵平衡 BST）。

### 📌 核心技巧：遍歷 (Traversal)
- **Pre-order (前序)**：先處理自己，再處理左右子樹。常用於樹的拷貝。
- **In-order (中序)**：先處理左子樹，再自己，再右子樹。**BST 的中序遍歷保證是由小到大排序的結果**（必考）。
- **Post-order (後序)**：先處理左右子樹，最後自己。常用於收集子樹資訊以決定根節點的行為（如：計算樹高）。

### 💻 經典模板與 Sample Code

#### 模板：BST 中序遍歷 (In-order) 驗證是否遞增
**Python**:
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isValidBST(root: TreeNode) -> bool:
    def inorder(node: TreeNode, lower: float, upper: float) -> bool:
        if not node:
            return True
        if node.val <= lower or node.val >= upper:
            return False
        # 往左走，將上限設為 node.val；往右走，將下限設為 node.val
        return inorder(node.left, lower, node.val) and inorder(node.right, node.val, upper)
    
    return inorder(root, float('-inf'), float('inf'))
```

#### 模板：反轉二元樹 (DFS Post-order)
**Python**:
```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None
        
    # 先反轉左右子樹
    left = invertTree(root.left)
    right = invertTree(root.right)
    
    # 把左右子樹交換
    root.left = right
    root.right = left
    
    return root
```
