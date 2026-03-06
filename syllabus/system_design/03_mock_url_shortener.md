# Google L4/L5 System Design Mock Interview — URL Shortener (bit.ly)
# Google L4/L5 系統設計模擬面試 — URL 短網址服務（bit.ly 規模）

**Interviewer:** Google System Design Interviewer (L5 Standard)
**Rating / 評級:** Hire

---

## 📋 Requirements | 需求釐清

### Scale | 規模
- **Writes:** 100 million URLs created/day → ~**1,160 writes/sec** (peak ~12,000/sec)
- **Reads:** 10 billion redirects/day → ~**115,000 reads/sec**
- **Read:Write ratio:** ~1,000 : 1 (read-heavy)
- **Short code format:** `short.ly/` + **7-character alphanumeric** (a–z, A–Z, 0–9) = 62⁷ ≈ **3.5 trillion** combos
- **Latency SLA:** redirect < **100ms at p99**

### Clarification Q&A | 釐清問答

| Question | Answer |
|---|---|
| Fixed format `short.ly/` + random code? | Yes, 7-char alphanumeric |
| Global users or specific timezone? | Global, no specific timezone |
| High concurrent traffic spikes? | Yes, assume **10x burst** above average |
| URL expiration? | Optional TTL; default = permanent |

---

## 🏗️ High-Level Architecture | 高層架構

```
Client
  → CDN Edge (optional 302 cache)
  → Load Balancer (geo-routed / latency-based)
  → Web Servers (stateless)
       ├─ ID Generator Cluster (ZooKeeper + range blocks)
       │    └─ Feistel Permutation f(N, K) → Base62
       ├─ Redis Cache (LRU, 24h TTL)
       └─ Cassandra / DynamoDB
            └─ Schema: short_code | long_url | key_version | ttl | created_at
```

---

## 🔄 Request Flows | 請求流程

### Write Flow (Create Short URL) | 寫入流程（建立短網址）
1. Client sends `POST /shorten` with `{ long_url, ttl? }`
2. Load Balancer → Web Server
3. Web Server retrieves next ID from its **local pre-fetched range**
4. Apply **Feistel permutation**: `N → N'` (scrambled, non-enumerable)
5. Encode `N'` as 7-char **Base-62** string → `short_code`
6. Write `{ short_code, long_url, key_version, ttl }` to DB
7. Return `short.ly/{short_code}` to client

### Read Flow (Redirect) | 讀取流程（重新導向）
1. Client navigates to `short.ly/{short_code}`
2. Load Balancer → Web Server
3. Check **Redis cache** for `short_code`
   - **Cache Hit:** Return `302 Found` with `long_url` immediately
   - **Cache Miss:** Query DB → populate cache → return `302 Found`

---

## ⚖️ Key Trade-off: 301 vs 302 | 關鍵取捨

| | 301 Moved Permanently | **302 Found ✅ (Chosen)** |
|---|---|---|
| Browser caching | Client caches forever | Client always hits server |
| Analytics tracking | ❌ Lost after first visit | ✅ Every click tracked |
| Target flexibility | ❌ "Burned" in browser cache | ✅ Can update destination anytime |
| Server load | Low (client-side cache) | Higher (mitigated by Redis) |

**Decision:** Choose **302** for analytics and control. Accept the server load; mitigate with aggressive Redis caching.
**決策：** 選擇 **302** 以支援分析追蹤與目標靈活性。透過 Redis 快取抵銷增加的伺服器負載。

---

## 🔑 ID Generator Design | ID 產生器設計

### Why Not Random + Collision Check? | 為何不用隨機 + 碰撞檢查？
At scale, the **Birthday Paradox** makes collision probability non-trivial. Each write would require a costly DB read-and-retry loop.
在此規模下，**生日悖論**使碰撞機率不可忽視。每次寫入都需要昂貴的 DB 讀取重試迴圈。

### Chosen: Distributed Range Allocation | 採用：分散式範圍分配

1. **Central counter store** (ZooKeeper / etcd) holds a global monotonic integer `N`.
2. A **Web Server at startup** requests a block of `10,000` IDs via atomic DB operation:
   ```sql
   UPDATE counters SET val = val + 10000 WHERE name = 'url_ids' RETURNING val;
   ```
3. Web Server generates IDs **locally in-memory** — zero network I/O per write.
4. When the block is exhausted, background-fetch the next block asynchronously.

**Benefits / 優點:**
- **Zero per-write latency** from ID generation (CPU-only, nanoseconds)
- **No collision checks** needed — uniqueness guaranteed by design
- **SPOF mitigation:** ZooKeeper cluster + Web Servers buffer thousands of IDs locally

---

## 🔒 Security: Non-Enumerable Codes | 安全性：防枚舉短碼

**Problem:** Sequential IDs produce guessable codes (`0000001`, `0000002`...). Anyone can scan the entire namespace.
**問題：** 序列 ID 產生可猜測的短碼，任何人都能掃描整個命名空間。

### Solution: Feistel Network Permutation | 解法：Feistel 網路排列

```
Sequential ID (N)
      ↓
Feistel f(N, K)   ← secret key K
      ↓
Scrambled ID (N') ← stored as DB primary key
      ↓
Base-62 encode → "aB3xK9f"
```

**Properties / 特性:**
- **Bijection (one-to-one):** Every `N` maps to exactly one `N'` → **zero collisions by math**
- **Non-enumerable:** Without key `K`, attacker cannot compute `N' + 1`
- **Zero latency:** Pure bitwise CPU operation — no network hop

### Key Rotation Risk & Mitigation | 密鑰輪換風險與緩解
- Store a `key_version` field in each DB record.
- On lookup, use `key_version` to select the correct key — all historical keys remain active in a versioned keystore.
- New URLs use the new key; existing URLs continue resolving via their stored `key_version`.

在每筆 DB 記錄中儲存 `key_version` 欄位。查詢時，依 `key_version` 選擇對應密鑰，所有歷史密鑰保留在版本化密鑰庫中。

---

## 🔴 Redis — See Standalone Reference | Redis 詳見獨立文件

> Detailed Redis strategies (Cache-Aside, LRU, Request Coalescing, AOF, ZSet, Pub/Sub) are documented in:
> **`system_design/redis_deep_dive.md`**
>
> Redis 詳細策略（旁路快取、LRU、請求合併、AOF、ZSet、Pub/Sub）請參閱：
> **`system_design/redis_deep_dive.md`**

**Quick summary for this system / 本系統快速摘要：**
- Strategy: **Cache-Aside** — app code manages Redis ↔ DB sync
- Eviction: **`allkeys-lru`**, TTL = 24h, pre-warm top-1% URLs on deploy
- Stampede protection: **Request Coalescing** with distributed lock on cold cache
- Write-through on URL creation to prevent **replication lag** issues



## 🌐 CDN (Content Delivery Network) | 內容傳遞網路

**Analogy / 比喻：**
> Your origin server is in Taipei. Without CDN, a user in New York must connect across the Pacific (~150ms RTT).
> CDN = **franchise branches**. A New York CDN node answers locally (~10ms).
>
> 你的源站在台北。沒有 CDN，紐約用戶需跨越太平洋（~150ms RTT）。CDN = **全球加盟店**，紐約用戶直接連到當地節點（~10ms）。

### Why CDN is Critical for URL Shortener | 為何對短網址服務至關重要

**Edge Computing (邊緣運算) — The L5 Key:**
Modern CDNs (e.g. Cloudflare Workers, AWS Lambda@Edge) can **execute code at the edge node**:

```javascript
// Runs at CDN edge, zero origin server contact
addEventListener('fetch', event => {
  const shortCode = event.request.url.split('/').pop();
  const longUrl = await edgeKV.get(shortCode);  // edge KV store
  if (longUrl) {
    return Response.redirect(longUrl, 302);  // served at <20ms globally
  }
  // Cache miss → forward to origin
});
```

**Result / 結果：**
- Cache Hit at CDN edge → redirect served in **< 20ms** globally, origin server **never touched**.
  CDN 邊緣快取命中 → 全球 **< 20ms** 回傳重新導向，源站**完全不受影響**。

---

## 🌍 Global Architecture Map | 全球佈局架構圖

```
User clicks short.ly/aB3xK9
         ↓
   [Geo-DNS]  ← detects user's IP region → returns nearest server IP
              偵測用戶 IP 來源 → 回傳最近伺服器 IP
         ↓
   [CDN Edge Node]  (nearest PoP, e.g. Tokyo for Asia users)
     └─ Cache HIT  → 302 redirect → Done ✅ (<20ms)
     └─ Cache MISS → forward to origin
         ↓
   [Load Balancer]  (regional)
         ↓
   [Web Server]  (stateless)
     └─ Redis HIT  → 302 redirect → Done ✅ (<50ms)
     └─ Redis MISS → query nearest Read Replica DB
         ↓
   [Read Replica DB]  (regional, e.g. AWS RDS replica in Tokyo)
     └─ Returns long_url → populate Redis → 302 redirect ✅
         ↑ async replication
   [Primary DB]  (e.g. us-east-1, handles all writes)
```

### A: Geo-DNS | 地理 DNS — 「數位交通警察」
- Detects user's IP region → returns the IP of the nearest server cluster.
  偵測用戶 IP 來源 → 回傳最近伺服器叢集的 IP。
- User in Asia → Taipei servers. User in Americas → New York servers.

### B: Read Replicas | 讀取副本 — 「資料的影分身」

| | Primary DB (主庫) | Read Replica (從庫) |
|---|---|---|
| **Role** | Handles all **Writes** 處理所有寫入 | Handles all **Reads** 處理所有讀取 |
| **Location** | Single region (e.g. us-east-1) | Multi-region (Tokyo, Frankfurt, São Paulo...) |
| **Sync** | — | Primary auto-replicates to replicas 主庫自動同步至從庫 |
| **User query** | Only for POST /shorten | For all GET /{shortCode} |

---

## ⚠️ Advanced Challenge: Replication Lag | 進階考題：複製延遲

**Question / 面試官問你：**
> "If replication lag causes a user's newly created short URL to not be found when they immediately try to access it — how do you handle this?"
>
> 「如果從庫複製延遲，導致使用者剛建立的短網址立刻訪問時查無資料，怎麼辦？」

**Root Cause / 根本原因：**
Write → Primary DB (us-east-1) ✅ but Read → Tokyo Replica (still replicating) → `404 Not Found` ❌
寫入成功到主庫，但讀取的東京從庫尚未同步完成 → 查無資料。

### Answer: Read-Your-Writes Consistency Strategies | 解法：讀己寫一致性策略

**Option 1 — Write-through to Redis (Recommended / 推薦)**
```
POST /shorten → write to Primary DB AND immediately write to Redis
```
- The creator's next read hits Redis → always consistent, regardless of DB lag.
  建立者的下一次讀取命中 Redis → 無論 DB 延遲，永遠一致。
- ✅ Zero latency impact. No code complexity on read path.

**Option 2 — Sticky Read (Route creator to Primary)**
- Tag the response with a `session_token` after creation.
- For the next N seconds, route that user's reads to the Primary DB, not replicas.
  建立後 N 秒內，將該用戶的讀請求導向主庫而非從庫。
- ⚠️ Adds routing complexity. Increases Primary DB read load.

**Option 3 — Monotonic Read Guarantee (from distributed DB)**
- Use a DB that provides **monotonic reads** (e.g. CockroachDB, Spanner).
  使用支援**單調讀**的分散式 DB（如 CockroachDB, Spanner）。
- Each read is tagged with a timestamp; replicas will not serve stale reads.
- ⚠️ Higher operational complexity and cost.

**L5 Answer Pattern / L5 回答模式:**
> "I would handle this with **write-through to Redis** on the write path. The newly created URL is immediately written to Redis with a short TTL. Any subsequent read — even before DB replication completes — will hit Redis and get a valid `302 Found`. This covers the creator's immediate access and the DB replica lag window simultaneously."
>
> 「我會在寫入路徑上採用 **write-through 到 Redis** 的策略。短網址建立後立即寫入 Redis 並設定短 TTL。後續任何讀取請求——即使在 DB 複製完成前——都能命中 Redis 並得到有效的 302 回應。這同時解決了建立者立即訪問與 DB 從庫延遲視窗兩個問題。」

---

## �📊 Final Evaluation | 最終評估

**Overall Rating / 總體評級:** `Hire`

| Dimension | Feedback |
|---|---|
| **Clarification** | ✅ 4 targeted, precise questions |
| **302 trade-off** | ✅ L5-quality: justified from analytics, control, and explicit sacrifice |
| **ID Generation** | ✅ Correct range allocation, Birthday Paradox reasoning, SPOF mitigation |
| **Security (FPP)** | ✅ Advanced: Feistel bijection, zero-latency, key risk identified |
| **Global distribution** | ⚠️ Not elaborated — CDN edge, geo-distributed DB replicas not addressed |
| **Cache eviction policy** | ⚠️ Redis proposed but TTL, LRU policy, cold-start not specified |
| **Key rotation lookup** | ⚠️ `key_version` field not mentioned — existing records would break |

### Actionable Corrections | 改善建議

1. **Key rotation requires `key_version` per record.**
   Store the key generation version alongside each URL so historical lookups remain valid after key rotation.
   密鑰輪換需要每筆記錄儲存 `key_version`，確保輪換後仍可查詢歷史記錄。

2. **Quantify your cache.**
   Always specify: eviction policy (LRU), TTL (e.g., 24h), pre-warming strategy for top-1% URLs.
   永遠要量化快取：驅逐策略（LRU）、TTL（如 24 小時）、前 1% URL 預熱策略。

3. **Address global latency explicitly.**
   For read-heavy global services: CDN edge nodes can serve 302 redirects directly, bypassing origin servers and dramatically reducing p99 latency.
   對於全球讀多的服務：CDN 邊緣節點可直接回應 302 重新導向，繞過源站，大幅降低 p99 延遲。
