import random

class RandomizedSet:
    def __init__(self):
        self.nums = []
        self.val_to_idx = {}

    def insert(self, val: int) -> bool:
        if val in self.val_to_idx:
            return False
        
        # O(1) append & map entry
        self.val_to_idx[val] = len(self.nums)
        self.nums.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.val_to_idx:
            return False
        
        # O(1) swap & pop logic
        idx_to_remove = self.val_to_idx[val]
        
        # Move last element to the target index
        self.nums[idx_to_remove] = self.nums[-1]
        self.val_to_idx[self.nums[-1]] = idx_to_remove
        
        # Cleanup
        self.nums.pop()
        del self.val_to_idx[val]
        
        return True

    def getRandom(self) -> int:
        # O(1) uniform selection
        return random.choice(self.nums)

if __name__ == "__main__":
    rs = RandomizedSet()
    
    # Test 1: Basic Insert
    print(f"Insert 1: {rs.insert(1)}")      # True
    print(f"Insert 2: {rs.insert(2)}")      # True
    print(f"Insert 1 (Duplicate): {rs.insert(1)}")  # False
    
    # Test 2: GetRandom (Should be 1 or 2)
    print(f"Random: {rs.getRandom()}")
    
    # Test 3: Remove last element (Edge case check)
    # If we remove 2, and 2 is the last element, the swap logic needs to be safe
    print(f"Remove 2: {rs.remove(2)}")      # True
    print(f"Random (must be 1): {rs.getRandom()}")
    
    # Test 4: Remove and Insert
    print(f"Insert 3: {rs.insert(3)}")      # True
    print(f"Remove 1: {rs.remove(1)}")      # True
    print(f"Random (must be 3): {rs.getRandom()}")
    
    # Test 5: Check non-existing remove
    print(f"Remove 100: {rs.remove(100)}")  # False