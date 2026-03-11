# Tech Guide: Redis in Distributed Systems (分散式系統中的 Redis)

**Topic / 主題:** High-performance Caching & Distributed State / 高效能快取與分散式狀態管理
**Level / 等級:** Google L4 / L5 Standard

---

## 1. Core Concepts (核心概念)

**English:**
Redis is an in-memory data structure store used as a database, cache, and message broker. In large-scale systems (like crawlers), it is critical for deduplication, task locking, and temporary state management.

**中文：**
Redis 是一個記憶體內資料結構存儲，可用作資料庫、快取和訊息代理。在大規模系統（如爬蟲）中，它對於去重、任務鎖定和臨時狀態管理至關重要。

---

## 2. Setup & Deployment (架設與部署)

### Standard Deployment (主從架構)
**English:** Use a Leader-Follower pattern for read scalability.
**中文：** 使用主從模式來擴展讀取能力。

```bash
# Basic Docker Setup
docker run --name redis-leader -d redis redis-server --appendonly yes
```

### Redis Cluster (大規模集群)
**English:** Shard data across multiple nodes to handle petabyte-scale metadata indexes or high-throughput Bloom Filters.
**中文：** 將數據分片至多個節點，以處理 PB 級的元數據索引或高吞吐量的布隆過濾器。

---

## 3. Implementation Example: Bloom Filter (程式實作：布隆過濾器)

**English:** Using Redis Bloom (ReBloom) for O(1) existence checks.
**中文：** 使用 Redis Bloom 進行 O(1) 的存在性檢查。

```python
import redis

class RedisDeduper:
    def __init__(self, host='localhost', port=6379):
        self.client = redis.Redis(host=host, port=port)

    def is_seen(self, url_hash: str) -> bool:
        # BF.EXISTS returns 1 if exists, 0 if not
        return self.client.execute_command('BF.EXISTS', 'url_bloom', url_hash) == 1

    def mark_seen(self, url_hash: str):
        self.client.execute_command('BF.ADD', 'url_bloom', url_hash)

# Usage in Crawler
deduper = RedisDeduper()
if not deduper.is_seen("hash_abc_123"):
    print("New URL found, safe to crawl.")
```

---

## 4. L4+ Deep Dive: Eviction & Persistence (L4+ 進階：淘汰與持久化)

| Policy (策略) | Description (說明) |
|---|---|
| **allkeys-lru** | **English:** Evict the least recently used keys. Best for caching. / **中文：** 淘汰最久未使用的 Key。適用於快取情境。 |
| **AOF + RDB** | **English:** Combine snapshotting (RDB) with command logging (AOF) for maximum durability. / **中文：** 結合快照與日誌，確保最大程度的資料持久性。 |
