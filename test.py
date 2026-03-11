from typing import List

class Node:
    def __init__(self, val=0, prev=None, next=None):
        self.val = val
        self.prev = prev
        self.next = next

class Solution:
    def countComponents(self, input_nodes: List[Node]) -> int:
        res = 0
        node_set = set(input_nodes)
        for node in input_nodes:
            if node.prev is None or node.prev not in node_set:
                res += 1
        return res

# --- Test harness ---
def create_doubly_list(arr):
    if not arr: return []
    nodes = [Node(val) for val in arr]
    for i in range(len(nodes)):
        if i > 0: nodes[i].prev = nodes[i-1]
        if i < len(nodes) - 1: nodes[i].next = nodes[i+1]
    return nodes

if __name__ == "__main__":
    # Original list: 0 <-> 1 <-> 2 <-> 3 <-> 4
    full_list = create_doubly_list([0, 1, 2, 3, 4])
    
    sol = Solution()
    
    # Case 1: [0, 1, 3] -> (0-1), (3) -> 2 components
    print(sol.countComponents([full_list[0], full_list[1], full_list[3]])) 
    
    # Case 2: [0, 2, 4] -> (0), (2), (4) -> 3 components
    print(sol.countComponents([full_list[0], full_list[2], full_list[4]]))
    
    # Case 3: [0, 1, 2, 3, 4] -> (0-1-2-3-4) -> 1 component
    print(sol.countComponents(full_list))
