import heapq

class StockPrice:

    def __init__(self):
        self.newest_value = None
        self.newest_timestamp = -1
        self.timestamp_price = {}
        self.min_price_heap = []
        self.max_price_heap = []

    def update(self, timestamp: int, price: int) -> None:
        if timestamp >= self.newest_timestamp:
            self.newest_timestamp = timestamp
            self.newest_value = price
        self.timestamp_price[timestamp] = price
        heapq.heappush(self.min_price_heap, (price, timestamp))
        heapq.heappush(self.max_price_heap, (-1 * price, timestamp))

    def current(self) -> int:
        # your implementation here
        return self.newest_value if self.newest_timestamp != -1 else -1

    def maximum(self) -> int:
        while self.max_price_heap and -1 * self.max_price_heap[0][0] != self.timestamp_price[self.max_price_heap[0][1]]:
            heapq.heappop(self.max_price_heap)
        return -1 * self.max_price_heap[0][0]

    def minimum(self) -> int:
        while self.min_price_heap and self.min_price_heap[0][0] != self.timestamp_price[self.min_price_heap[0][1]]:
            heapq.heappop(self.min_price_heap)
        return self.min_price_heap[0][0]


# --- Test harness ---
if __name__ == "__main__":
    stock = StockPrice()
    stock.update(1, 10)
    stock.update(2, 5)
    print(stock.current())  # Expected: 5
    print(stock.maximum())  # Expected: 10
    
    stock.update(1, 3)      # Correction: timestamp 1 is now price 3
    print(stock.maximum())  # Expected: 5 (since 10 was overwritten)
    
    stock.update(4, 2)
    print(stock.minimum())  # Expected: 2
