from typing import List
from collections import deque

class Solution:
    def minMaxSubarray(self, nums: List[int], k: int) -> int:
        res = float('inf')
        data = deque([])
        for idx, num in enumerate(nums):
            while data and nums[data[-1]] <= num:
                data.pop()
            data.append(idx)
            
            if data[0] <= idx - k:
                data.popleft()
            
            if idx >= k - 1:
                res = min(res, nums[data[0]])
        return res

# --- Test harness ---
if __name__ == "__main__":
    sol = Solution()
    print(sol.minMaxSubarray([1, 3, 1, 2, 0, 5], 3))  # Expected: 2
    print(sol.minMaxSubarray([1, 1, 1, 1], 2))          # Expected: 1
    print(sol.minMaxSubarray([5], 1))                    # Expected: 5
