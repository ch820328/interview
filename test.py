class Node:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node
    
    def _add_to_head(self, node: Node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.val

    def put(self, key, val):
        if key in self.cache:
            node = self.cache[key]
            node.val = val
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
            
            new_node = Node(key, val)
            self._add_to_head(new_node)
            self.cache[key] = new_node


if __name__ == "__main__":
    cache = LRUCache(capacity=2)
    cache.put(1, 1)    # cache is {1=1}
    cache.put(2, 2)    # cache is {1=1, 2=2}
    print(cache.get(1))       # returns 1
    cache.put(3, 3)    # evicts key 2, cache is {1=1, 3=3}
    print(cache.get(2))       # returns -1 (not found)
    cache.put(4, 4)    # evicts key 1, cache is {4=4, 3=3}
    print(cache.get(1))       # returns -1 (not found)
    print(cache.get(3))       # returns 3
    print(cache.get(4))       # returns 4
