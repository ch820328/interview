from typing import List
import uuid6

# 數據層：解耦存儲
content_hash_map = {}

class Node:
    def __init__(self, name):
        self.name = name

class NodeDirectory(Node):
    def __init__(self, name):
        super().__init__(name=name)
        self.dirs = {}   # 子目錄
        self.files = {}  # 子檔案
    
class NodeFile(Node):
    def __init__(self, name):
        super().__init__(name=name)
        self.uuid_v7 = str(uuid6.uuid7())
        self.content = '' # 初始使用內聯存儲
        self.inlined = True

    def append(self, content):
        if not self.inlined:
            content_hash_map[self.uuid_v7] += content
        elif len(self.content) + len(content) > 4096:
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
        if path == "/": return []
        return [p for p in path.split("/") if p]

    def ls(self, path: str) -> List[str]:
        parts = self._get_parts(path)
        curr = self.root
        
        # 1. 導航到倒數第二層或目標層
        for i, p in enumerate(parts):
            if p in curr.dirs:
                curr = curr.dirs[p]
            elif p in curr.files:
                # 如果路徑指向的是檔案，ls 必須只回傳該檔名
                if i == len(parts) - 1:
                    return [p]
                return []
            else:
                return []

        # 2. 如果導航結束，curr 是目錄
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


# --- Test Selection ---
if __name__ == "__main__":
    fs = FileSystem()
    
    # Case 1: Simple mkdir and ls
    print(fs.ls("/")) # []
    fs.mkdir("/a/b/c")
    fs.addContentToFile("/a/b/c/d", "hello")
    print(fs.ls("/")) # ['a']
    print(fs.readContentFromFile("/a/b/c/d")) # "hello"

    # Case 2: Sorted output and directory vs file
    fs.addContentToFile("/a/b/c/e", "world")
    print(fs.ls("/a/b/c")) # ['d', 'e']
    print(fs.ls("/a/b/c/d")) # ['d']
