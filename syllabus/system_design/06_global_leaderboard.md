# System Design: Global Real-Time Leaderboard (全球即時排行榜)

**Target Level:** Google L4+ (Software Engineer III / Senior)
**Focus Area:** Hybrid Architecture, Sharding Strategies, Hot Key Mitigation, Scalability Trade-offs

---

## 🏆 The Problem (50 Million DAU Leaderboard)
Design the backend for a global real-time leaderboard for a massive multiplayer online game (e.g., Apex Legends or Fortnite) with 50M Daily Active Users. 
- Scores are updated 10+ times a day per user.
- Players can query the **Global Top 100**.
- Players can query their **Own Rank**.
- Latency for reading must be strictly **< 50ms**.

---

## 🏗️ The L4+ Hybrid Architecture (混合架構)

To achieve both high throughput (writes) and extreme low latency (reads), a single database (either pure SQL or pure Redis) is insufficient. We must decouple storage from real-time compute.

### 1. Storage Layer (Persistent SQL)
SQL acts as the absolute Source of Truth for `(user_id, score)`. 
- **The Challenge:** 50M active users writing 10 times a day will melt a single SQL instance.
- **The Solution:** We must shard the SQL database horizontally.
- **The Trade-off: Range Sharding vs. Hash Sharding:**
  - *Range Sharding (by score):* Easy to query Top 100, but creates catastrophic **Write Hotspots** when a new season starts and everyone is at 0 score (DB1 crashes, DB2 is idle).
  - *Hash Sharding (by `user_id`):* Guarantees perfectly uniform write distribution. We choose this to protect system stability. 
  - *The Catch:* Hash sharding makes querying the "Global Top 100" impossible without an expensive Scatter-Gather across all SQL nodes.

### 2. The Ranking Overlay Service (Redis ZSet)
To solve the SQL Scatter-Gather problem, we introduce a fast, in-memory **Ranking Overlay Service** using Redis Sorted Sets (`ZSet`).

**The Data Flow (Asynchronous Dual-Write):**
1. Game Server finishes a match -> Sends `(user_id, score)` to **Kafka (Message Queue)**.
2. An async worker consumes the Kafka stream.
3. It writes the data to the SQL Storage Layer (batching inserts for efficiency).
4. Simultaneously, it updates the Ranking Overlay Service (Redis `ZADD`).

---

## 💣 Key L4+ Pressure Tests & Defense Strategies

If you naively put 50M users into a single Redis `ZSet` named `leaderboard`, that single Redis shard will become a catastrophic CPU and Network bottleneck (Single Point of Failure).

### Defense 1: Tiered Leaderboards & Bucket Sharding
Instead of one massive global ranking, we **decompose the duties (功能拆解)**:

1. **Top-Tier Global Set (熱點層):** 
   We only maintain the exact ranking for the **Global Top 10,000** players in a dedicated Redis `ZSet`. Because the cardinality is extremely small, memory and CPU overhead are trivial. When users query "Top 100", we fetch from this tier in 1-5ms.

2. **Sharded Rank Buckets (長尾層):** 
   For the remaining 49.99 million players, we shard them into score buckets (e.g., Bucket A: 0-1000 pts, Bucket B: 1001-2000 pts). The system only tracks how many total users are in each bucket.

### Defense 2: Approximate Rank (近似排名)
When a player with an average score asks for their "Own Rank", we query the SQL database for their exact score. Then, we calculate the sum of players in all buckets above them. 
We return an **Approximate Rank** (e.g., "Rank: 15,231,000+" or "Top 30%").
- *The Senior Rationale:* Delivering a pixel-perfect rank for the 15-millionth player provides zero product value but incurs massive architectural tax. Approximating the long-tail is a textbook product/engineering trade-off that interviewers love.

---

## 📈 Summary Architecture Flow
1. **Write:** `Game Server` -> `Kafka` -> `Worker` -> (`SQL Hash Shard` + `Redis Top-10k ZSet` + `Redis Score Buckets`)
2. **Read Top 100:** `Client` -> `API Gateway` -> `Redis Top-10k ZSet` (O(1) latency).
3. **Read Own Rank:** 
   - Get score from `SQL Hash Shard`.
   - If score is in Top-10k, fetch exact rank from `Redis Top-10k ZSet`.
   - If not, sum the populations of higher `Redis Score Buckets` to provide an Approximate Rank.
