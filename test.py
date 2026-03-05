from collections import Counter, deque

import heapq

class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        wordSet = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        
        dp[0] = True

        for i in range(1, n + 1):
            for j in range(i):
                if dp[j] and s[j:i] in wordSet:
                    dp[i] = True
                    break 
        
        return dp[n]

print(Solution().wordBreak(s = "catsanddog", wordDict = ["cats","dog","sand","and","cat"]))
