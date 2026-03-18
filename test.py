from typing import List
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        t_count = Counter(t)
        t_char_need = len(t_count.keys())

        min_length = float('inf')
        min_length_string = ''
        left = 0
        for right in range(len(s)):
            if s[right] in t_count:
                t_count[s[right]] -= 1
                if t_count[s[right]] == 0:
                    t_char_need -= 1
                while t_char_need == 0:
                    if min_length > right - left + 1:
                        min_length_string = s[left:right + 1]
                        min_length = right - left + 1
                        if min_length == len(t):
                            return min_length_string
                    if s[left] in t_count:
                        t_count[s[left]] += 1
                        if t_count[s[left]] == 1:
                            t_char_need += 1
                    left += 1
        return min_length_string

            

# --- Test harness ---
if __name__ == "__main__":
    sol = Solution()
    
    # Normal case
    print(f'Test 1: {sol.minWindow("ADOBECODEBANC", "ABC")}')  # Expected: "BANC"
    
    # Small single-character case
    print(f'Test 2: {sol.minWindow("a", "a")}')  # Expected: "a"
    
    # Edge case - Not enough characters
    print(f'Test 3: {sol.minWindow("a", "aa")}')  # Expected: ""