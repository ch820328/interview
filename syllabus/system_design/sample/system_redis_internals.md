# Redis Deep Dive | Redis 深度解析

> Redis 不僅是 Key-Value 儲存，它是一台「**記憶體運算引擎**」。
> Redis is not just a key-value store — it is an **in-memory computation engine**.

---

## Strategy 1: Cache-Aside (旁路快取) ← Most Stable | 最穩定

**The pattern / 模式：**

```
Read Request
     ↓
 Check Redis
   ↙      ↘
HIT        MISS
 ↓           ↓
Return    Query DB
          ↓
       Write result to Redis
          ↓
        Return
```

**Why it's preferred / 為何首選：**
- Application code controls the sync between Redis and DB.
  應用程式碼負責 Redis 與 DB 的同步。
- If Redis crashes, the system **degrades gracefully** — it still serves from DB (just slower). It does **not** crash.
  若 Redis 崩潰，系統**優雅降級**，仍可從 DB 提供服務（只是較慢）。系統**不會**直接崩潰。

---

## Strategy 2: LRU Eviction Policy | LRU 驅逐策略

**Analogy / 比喻：**
> Your desk (Redis memory) is small. The library (DB disk) is huge.
> LRU = when the desk is full, put the **least recently opened book** back on the shelf, keep the **hottest books** on the desk.
>
> 你的書桌（Redis 記憶體）很小，圖書館（DB 磁碟）很大。LRU = 桌子滿了，把「最久沒翻開的書」放回架上，讓「最熱門的書」留在桌上。

**Typical configuration / 典型設定：**
```
maxmemory-policy allkeys-lru
TTL per key: 24 hours
Pre-warm on deploy: top-1% most-accessed keys
部署時預熱：存取量前 1% 的熱門 Key
```

---

## Strategy 3: Request Coalescing | 請求合併（防快取擊穿）

**Problem — Cache Stampede (快取擊穿):**
When a viral key's cache entry expires, **10,000 simultaneous requests** all see a Cache Miss and hammer the DB with identical queries.
當熱點 Key 的快取過期，**同時 10,000 個請求**都看到 Cache Miss，對 DB 發出相同查詢。

**Solution — Coalescing with a distributed lock / 使用分散式鎖合併請求：**
```
Request 1  → acquires lock → queries DB → fills Redis → releases lock
                                                              ↓
Requests 2–9999  → see lock → wait (or return "pending") → read Redis after lock released
```

**Why it matters / 為何重要：**
- Without coalescing: DB receives 10,000 identical queries simultaneously → potential overload.
  未合併：DB 同時收到 10,000 次相同查詢 → 可能過載。
- With coalescing: DB receives **exactly 1 query**. All others wait for Redis to be populated.
  合併後：DB 只收到 **1 次查詢**，其餘等待 Redis 填滿即可。

---

## Advanced Toolbox | Redis 進階工具箱

| Feature | Use Case | Key Command |
|---|---|---|
| **Sorted Sets (ZSet)** | Leaderboard / Top-N hottest keys in 24h 排行榜 / 24小時熱門排行 | `ZINCRBY`, `ZREVRANGE` O(log N) |
| **Pub/Sub** | Real-time push notifications without polling DB 即時推播，無需輪詢 DB | `PUBLISH`, `SUBSCRIBE` |
| **AOF Persistence** | Replay write log on restart — survives crashes 重啟後重放日誌，資料不丟失 | `appendonly yes` |
| **RDB Snapshots** | Periodic full-state backup 定期全量快照備份 | `BGSAVE` |
| **Distributed Lock** | Request coalescing; prevent double-write 請求合併、防止重複寫入 | `SET key val NX PX <ms>` |
| **Streams** | Event sourcing / audit log 事件溯源 / 稽核日誌 | `XADD`, `XREAD` |

> **Common misconception / 常見誤解:** Redis does NOT lose all data on crash if AOF is enabled. It replays the write log on restart.
> 若啟用 AOF，Redis 重啟後會自動重放日誌，資料不會全部消失。

---

## Persistence Modes Comparison | 持久化模式比較

| Mode | How it works | Data loss risk | Performance cost |
|---|---|---|---|
| **No persistence** | Pure in-memory; lost on crash 純記憶體，重啟即消失 | 100% on crash | ✅ Fastest |
| **RDB (Snapshot)** | Saves full snapshot every N seconds 每 N 秒儲存完整快照 | Up to N seconds of data | ✅ Low |
| **AOF (Append Only File)** | Logs every write command; replays on boot 記錄每條寫入指令，重啟時重放 | Near-zero (configurable fsync) | ⚠️ Slightly higher |
| **RDB + AOF** | Best of both worlds | Near-zero | ⚠️ Moderate |

**Recommendation for production URL shortener / 短網址服務生產環境建議：**
Use **AOF with `everysec` fsync** — at most 1 second of data loss, with acceptable write throughput.
使用 **AOF 搭配 `everysec` fsync**：最多丟失 1 秒資料，寫入吞吐量可接受。

---

## Common Interview Questions | 常見面試考題

| Question | L5 Answer Summary |
|---|---|
| Redis crashes — do you lose all data? | No, if AOF is enabled it replays on restart. 啟用 AOF 則重放日誌，資料不丟失。 |
| Cache Stampede / 快取擊穿 — how do you solve it? | Distributed lock + Request Coalescing. Only 1 request queries DB; others wait. 分散式鎖合併請求。 |
| How do you build a real-time leaderboard? | Redis ZSet with `ZINCRBY` + `ZREVRANGE`. O(log N) per update. |
| Cache eviction when memory is full? | `allkeys-lru` — evicts the least recently used key. LRU 驅逐最久未存取的 Key。 |
| How do you prevent a hot key bottleneck? | Local in-process cache (L1) in front of Redis to absorb burst traffic. 在 Redis 前加本地快取（L1）吸收爆流量。 |

---

## ⚖️ Trade-Off Analysis | 所有決策的取捨分析

> An L5+ engineer never just says *what* they chose — they articulate *what they gave up*.
> L5+ 工程師不只說「我選了什麼」，更要說清楚「我放棄了什麼」。

---

### Decision 1: Cache-Aside vs Write-Through vs Write-Behind

| Strategy | ✅ What You Gain | ❌ What You Sacrifice |
|---|---|---|
| **Cache-Aside** ✅ | Graceful degradation if Redis dies; app controls sync. Redis 掛掉系統仍可從 DB 服務 | Cold miss on first read. Stale data if DB updated bypassing app. 初次請求 miss；繞過 app 更新 DB 可能讀到舊資料 |
| **Write-Through** | Redis + DB always in sync on every write. 寫入同時更新兩端，永遠一致 | Write latency doubles. Wastes cache if data rarely read. 寫入延遲加倍；冷資料浪費快取空間 |
| **Write-Behind** | Ultra-fast writes — only write Redis; DB async later. 寫入極快 | Data loss if Redis crashes before flushing. Complex guarantees. Redis 崩潰前未 flush 則資料丟失 |

**Verdict:** Cache-Aside is default for read-heavy. Write-Through for zero-stale-tolerance (financial). Write-Behind only when write speed dominates and loss is acceptable.

---

### Decision 2: LRU vs Other Eviction Policies

| Policy | Best For | ❌ Trade-Off |
|---|---|---|
| **`allkeys-lru`** ✅ | General read caches | May evict still-relevant keys during traffic bursts. 爆流量時可能驅逐仍有價值的 Key |
| **`volatile-lru`** | Only TTL-tagged keys should be evicted | Non-TTL keys never evicted → memory never freed. 無 TTL 的 Key 永不被驅逐 |
| **`allkeys-lfu`** | Stable hot keys (Zipf distribution) | Better hit rate, but requires Redis 4.0+; poor for bursty new keys. |
| **`noeviction`** | Critical data that must be preserved | Writes fail when memory full. 記憶體滿時寫入直接失敗 |

---

### Decision 3: AOF vs RDB Persistence

| Mode | ✅ Gain | ❌ Sacrifice |
|---|---|---|
| **RDB** | Fast restart. Low I/O during normal ops. 重啟快，平時 I/O 低 | Lose up to N minutes of writes. 可丟失 N 分鐘資料 |
| **AOF `everysec`** ✅ | At most 1s data loss. Readable log. 最多丟失 1 秒 | Slightly higher disk I/O. File grows (needs `BGREWRITEAOF`). |
| **AOF `always`** | Zero data loss — every write fsynced | 2–10× write throughput drop. 寫入吞吐量降 2–10 倍 |
| **RDB + AOF** | Best recovery guarantee | Highest I/O and CPU. Reserve for critical data. |

---

### Decision 4: Request Coalescing (Distributed Lock)

| Approach | ✅ Gain | ❌ Sacrifice |
|---|---|---|
| **No coalescing** | Simple code, no latency for request #1 | N identical DB queries on cache miss → stampede. DB 擊穿風險 |
| **Distributed Lock** ✅ | Exactly 1 DB query per miss. Protects DB. | Requests 2–N wait → tail latency increases. Lock adds complexity. 尾部延遲上升；實作複雜 |
| **Probabilistic Early Expiry** | No lock needed; refreshes before expiry | Some stale reads. Harder to reason about. 仍可能讀到舊資料 |

---

## 🚀 L5+ Scaling Concepts | L5+ 擴展進階概念

### A: Redis Cluster — Slot-based Sharding | 水平分片

**When:** Single node RAM or CPU ceiling (~100GB or ~1M ops/sec).

```
Key → CRC16(key) % 16384 → Slot → Node
Node 1: Slots 0–5460  |  Node 2: Slots 5461–10922  |  Node 3: Slots 10923–16383
```

| | Detail |
|---|---|
| ✅ **Gain** | Linear horizontal scale, no single-node bottleneck. 線性擴展，無單點瓶頸 |
| ❌ **Sacrifice** | Multi-key ops (`MGET`) fail across nodes. Must use hash tags `{user}:key` to co-locate related keys. 跨節點多 Key 操作失敗；需用 hash tag 確保相關 Key 在同一節點 |

---

### B: Pipelining — Batch RTT Reduction | 批次指令減少 RTT

**When:** Bulk reads of many keys at once (e.g. 50 short URLs in one request).

```
Without:  [CMD1]→RTT→[CMD2]→RTT→[CMD3]  (N × RTT)
With:     [CMD1|CMD2|CMD3]→RTT→[RES1|RES2|RES3]  (1 × RTT)
```

| | Detail |
|---|---|
| ✅ **Gain** | N × RTT reduced to ~1 RTT for bulk ops. 批次操作延遲從 N×RTT 降至約 1×RTT |
| ❌ **Sacrifice** | Results arrive together; cannot branch on intermediate values. Large pipelines spike client memory. 無法基於中間結果分支；Pipeline 太大暴增客戶端記憶體 |

---

### C: L1 (Local) + L2 (Redis) Multi-Level Cache | 多層快取

```
Request → [L1: In-process ~50MB, TTL 1–5s]  ← top 0.1% hot keys, zero network hop
               ↓ miss
           [L2: Redis Cluster, TTL 24h]        ← top 1–10% hot keys
               ↓ miss
           [DB Read Replica]
```

| | Detail |
|---|---|
| ✅ **Gain** | Absorbs extreme hot-key traffic with zero network I/O. 無網路開銷，吸收極端熱點流量 |
| ❌ **Sacrifice** | L1 is per-process → different servers have different L1 states. Stale window = L1 TTL. 不同實例 L1 狀態不一致，舊資料視窗 = L1 TTL |
| **Rule** | L1 TTL must be short enough that the inconsistency window is within your SLA (typically 1–5s). |

---

### D: Connection Pooling | 連接池

**Problem:** Fresh TCP connection per request = ~1ms handshake × 115,000 RPS = unacceptable overhead.

| | Detail |
|---|---|
| ✅ **Gain** | Reuses warm connections → eliminates handshake → lower, stable p99 latency. 消除握手，降低 p99 延遲 |
| ❌ **Sacrifice** | Pool too small → queue. Pool too large → Redis exhausts file descriptors. 太小導致排隊；太大耗盡 Redis 檔案描述子 |
| **Tuning** | `pool_size ≈ avg_redis_latency_ms × target_RPS_per_instance / 1000` |

---

## 🗺️ Decision Map | 決策地圖

```
Caching strategy?
  ├─ Redis may crash, read-heavy          → Cache-Aside ✅
  ├─ Must be consistent on every write    → Write-Through
  └─ Ultra-fast writes, tolerate loss     → Write-Behind

Eviction policy?
  ├─ General cache                        → allkeys-lru ✅
  ├─ Some keys must never be evicted      → volatile-lru
  └─ Stable hot-key distribution          → allkeys-lfu

Persistence?
  ├─ Tolerate ~1s loss, need performance  → AOF everysec ✅
  ├─ Zero loss, perf is secondary         → AOF always
  ├─ Fast restart priority                → RDB
  └─ Critical system, no compromise       → RDB + AOF

Scale beyond single node?
  ├─ > 100GB or > 1M ops/sec             → Redis Cluster (Sharding)
  ├─ Batch reads of many keys             → Pipelining
  ├─ Extreme hot-key bottleneck           → L1 Local + L2 Redis
  └─ High-RPS connection overhead         → Connection Pooling
```
