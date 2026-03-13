# Coding: Design In-Memory File System (程式設計：記憶體檔案系統設計)

**Topic / 主題:** Trie / Tree Design & Memory Optimization (字典樹與記憶體優化)
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-13

---

## 1. Problem Statement & Constraints (問題描述與約束)

### English:
Design a data structure that simulates an in-memory file system. Support `ls`, `mkdir`, `addContentToFile`, and `readContentFromFile`. 
- Paths always start with `/`. 
- `ls` must return sorted names for directories and the file name itself for files.
- `mkdir` and `addContentToFile` should create missing parent directories.

### 中文：
設計一個模擬記憶體內檔案系統的資料結構。支援 `ls`、`mkdir`、`addContentToFile` 與 `readContentFromFile`。
- 路徑一律以 `/` 開頭。
- `ls` 對於目錄應回傳排序後的名稱清單；對於檔案則回傳檔案本身的名稱。
- `mkdir` 與 `addContentToFile` 應能建立缺失的父目錄。

---

## 2. Clarification Q&A (澄清問答)

| Question (問題) | Answer (回答) |
|---|---|
| **English:** How to handle multiple slashes (e.g., `//a///b`)? | **English:** Normalize by treating them as a single slash. |
| **中文：** 如何處理多個斜線（例如 `//a///b`）？ | **中文：** 進行正規化處理，將其視為單一斜線。 |
| **English:** Is `ls /a` the same as `ls /a/`? | **English:** Yes, they are equivalent for directory listing. |
| **中文：** `ls /a` 與 `ls /a/` 是否相同？ | **中文：** 是的，讀取目錄時它們是等價的。 |

---

## 3. Brute Force vs Optimal (暴力解與最優解)

| Feature (特性) | Brute Force (暴力解) | Optimal (最優解 - Trie/Hybrid) |
|---|---|---|
| **Lookup (查詢)** | Hash Map of full paths: $O(N)$ lookup. | Trie structure: $O(L)$ where $L$ is path depth. |
| **Space (空間)** | High redundancy in path strings. | Prefix sharing reduces memory overhead. |
| **Optimization (優化)** | None. | **Hybrid Inline/UUID Storage:** Decouple huge files using UUIDs. |

---

## 4. Implementation (程式實作)

```python
from typing import List
import uuid

# Global decoupled storage for large contents
content_hash_map = {}

class Node:
    def __init__(self, name):
        self.name = name

class NodeDirectory(Node):
    def __init__(self, name):
        super().__init__(name=name)
        self.dirs = {}   # Child directories
        self.files = {}  # Child files
    
class NodeFile(Node):
    def __init__(self, name):
        super().__init__(name=name)
        self.uuid_v7 = str(uuid.uuid4()) # Assume UUIDv7 or v4
        self.content = '' # Inline storage for small files
        self.inlined = True

    def append(self, content):
        if not self.inlined:
            content_hash_map[self.uuid_v7] += content
        elif len(self.content) + len(content) > 4096: # 4KB threshold
            content_hash_map[self.uuid_v7] = self.content + content
            self.content = None
            self.inlined = False
        else:
            self.content += content

    def get_content(self):
        return self.content if self.inlined else content_hash_map[self.uuid_v7]

class FileSystem:
    def __init__(self):
        self.root = NodeDirectory('/')

    def _get_parts(self, path: str) -> List[str]:
        return [p for p in path.split("/") if p]

    def ls(self, path: str) -> List[str]:
        parts = self._get_parts(path)
        curr = self.root
        
        for i, p in enumerate(parts):
            if p in curr.dirs:
                curr = curr.dirs[p]
            elif p in curr.files:
                if i == len(parts) - 1:
                    return [p]
                return []
            else:
                return []

        res = list(curr.dirs.keys()) + list(curr.files.keys())
        return sorted(res)

    def mkdir(self, path: str) -> None:
        parts = self._get_parts(path)
        curr = self.root
        for p in parts:
            if p not in curr.dirs:
                curr.dirs[p] = NodeDirectory(p)
            curr = curr.dirs[p]

    def addContentToFile(self, filePath: str, content: str) -> None:
        parts = self._get_parts(filePath)
        curr = self.root
        for p in parts[:-1]:
            if p not in curr.dirs:
                curr.dirs[p] = NodeDirectory(p)
            curr = curr.dirs[p]
        
        file_name = parts[-1]
        if file_name not in curr.files:
            curr.files[file_name] = NodeFile(file_name)
        curr.files[file_name].append(content)

    def readContentFromFile(self, filePath: str) -> str:
        parts = self._get_parts(filePath)
        curr = self.root
        for p in parts[:-1]:
            if p not in curr.dirs: return ""
            curr = curr.dirs[p]
        
        file_name = parts[-1]
        if file_name in curr.files:
            return curr.files[file_name].get_content()
        return ""
```

---

## 5. Dry Run Table (測試執行表)

| Operation (操作) | Path (路徑) | State Change (狀態變化) | Result (結果) |
|---|---|---|---|
| `mkdir` | `/a/b` | `root.dirs['a'].dirs['b']` created | `None` |
| `addContent` | `/a/c` | `root.dirs['a'].files['c']` created | `None` |
| `ls` | `/a` | Scans `a.dirs` and `a.files` | `['b', 'c']` |

---

## 6. L4/L5 Follow-up Discussion (L4/L5 進階探討)

### Concurrency (併發控制)
**English:** 
Implement node-level Reader-Writer locks. Use Shared Locks for `ls/read` and Exclusive Locks for `mkdir/append`.
**中文：**
實作節點級別的讀寫鎖。`ls/read` 使用共享鎖 (Shared Lock)，`mkdir/append` 使用排他鎖 (Exclusive Lock)。

### Scaling `ls` (ls 的性能擴展)
**English:** 
If directory size exceeds 100k+ entries, $O(K \log K)$ sorting becomes a bottleneck. Use a **SortedDict** or B-Tree to maintain order during insertion ($O(\log K)$) to keep `ls` at $O(K)$.
**中文：**
若目錄大小超過 10 萬項，$O(K \log K)$ 的排序將成為瓶頸。應使用 **SortedDict** 或 B-Tree 在插入時維持順序 ($O(\log K)$)，使 `ls` 降至 $O(K)$。

---

## 7. Evaluation & Corrections (評估與改進)

1. **Overall Rating:** **Strong Hire**
2. **Actionable Corrections:** 
   - **English:** Be careful with recursive cleanup in `rm()`; ensure UUIDs are purged from global hash map to avoid memory leaks.
   - **中文：** 實作 `rm()` 時需注意遞迴清理；確保從全域雜湊表中刪除 UUID 以避免記憶體洩漏。

---

## 8. Technical Term Dictionary (技術名辭典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Trie** | Tree structure for prefix matching | 字典樹 |
| **Inlined Storage** | Keeping small data directly in metadata nodes | 內聯存儲 |
| **UUID** | Universally Unique Identifier | 通用唯一辨識碼 |
| **Memory Fragmentation** | Wasted memory due to small allocations | 記憶體碎片化 |
