
class Solution:
    def minEatingSpeed(self, piles : list[int], h: int) -> int:
        def get_hours_needed(speed):
            return sum(((p - 1) // speed + 1) for p in piles)
        l = 1
        r = max(piles)

        while r > l:
            mid = (l + r) // 2
            if get_hours_needed(mid) <= h:
                r = mid
            else:
                l = mid + 1
        return r
      
if __name__ == "__main__":
    print(Solution().minEatingSpeed(piles = [30,11,23,5,4], h = 5))
    print(Solution().minEatingSpeed(piles = [3,6,7,11], h = 8))