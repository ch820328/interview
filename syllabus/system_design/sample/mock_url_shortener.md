# Google System Design Syllabus — URL Shortener (Ultimate Guide)
# Google 系統設計面試指南 — URL 短網址服務（L4 / L5 終極整合版）

這份文件整合了 L4 穩健的容量估算基礎與 L5 深入的分散式架構防禦策略。

---

## 1. Requirements & Scale / 系統需求與規模

**English:**
- **Functional:** Create a 7-character Base62 alias for a long URL ($62^7 \approx 3.5$ trillion combos). Redirect short URL to long URL.
- **Non-Functional:** Highly available (99.99%), extremely low latency reads (<20ms with CDN). Read-heavy system (100:1 ratio).
- **Scale Math:** 
  - Writes: 100M URLs/month $\approx$ 40 Avg QPS (200 Peak QPS).
  - Reads: 10B redirects/month $\approx$ 4,000 Avg QPS (20,000 Peak QPS).
  - Storage: 100M/month * 12 * 5 years = 6 Billion URLs. 6B * 150 Bytes $\approx$ **900 GB** total storage.
  - Cache: 20% of daily read traffic $\approx$ **16GB Redis Cluster**.

**Chinese (Traditional):**
- **功能性需求：** 將長網址縮短為 7 個字元 (Base62)。造訪短網址時重定向至長網址。
- **非功能性需求：** 高可用性 (99.99%)、極低延遲讀取 (CDN 支援下 <20ms)。讀多寫少 (100:1)。
- **系統規模與估算：**
  - 寫入：每月新增 1 億筆 $\approx$ 40 平均 QPS (尖峰 200)。
  - 讀取：每月 100 億次 $\approx$ 4,000 平均 QPS (尖峰 20,000)。
  - 存儲容量：保留 5 年 = 60 億筆網址。60 億 * 150B $\approx$ **900 GB**。
  - 快取：每日 20% 讀取流量 $\approx$ 需配置 **16GB Redis 叢集**。

---

## 2. Architecture Diagram / 全球佈局架構圖

```text
User clicks short.ly/aB3xK9
         ↓
   [Geo-DNS]  ← 偵測用戶 IP 來源 → 回傳最近 CDN 或伺服器 IP
         ↓
   [CDN Edge Node]  (e.g., Cloudflare Workers / AWS Lambda@Edge)
     ├─ Cache HIT  → 返回 302 重新導向 → Done ✅ (<20ms, 源站零負載)
     └─ Cache MISS → 轉發至源站
         ↓
   [Load Balancer]
         ↓
   [Web Server] (Stateless API)
     ├─ [ID Generator (ZooKeeper Counter)] ← 批次領取號碼牌 (Block Allocation)
     │   └─ [Feistel Permutation] ← 加密混淆，防止循序掃描
     ├─ [Redis Cluster (16GB)] ← Cache-Aside & Write-Through
     └─ [NoSQL Database (Primary in US, Read Replicas globally)]
```

---

## 3. Core Trade-offs & Architecture Decisions / 核心權衡與決策

### A. Redirect Status: 301 vs 302 Found ✅
- **Decision:** Use **302** (Found / Temporary Redirect).
- **Why (為何選 302)：** 301 會被瀏覽器永久快取，這會導致伺服器無法攔截後續的點擊請求，從而**失去追蹤點擊數據 (Analytics)** 的能力。對於短網址服務，數據追蹤是核心商業需求，因此必須承擔較高的伺服器負載來換取精準的分析數據 (並使用 Redis + CDN 來抵銷負載壓力)。

### B. ID Generation: Ticket Server vs Others ✅
- **Decision:** **Distributed Block Allocation (ZooKeeper / DB Counter)**. Web servers claim chunks of 10,000 IDs to generate locally. 
- **The Snowflake Trap (致命陷阱)：** Snowflake 產生的 ID 是 64-bit 整數。若將 64-bit 整數轉為 Base62，長度將高達 11+ 個字元，**直接違反題目「7 碼」的長度限制**。
- **The MD5 Hash Trap (雜湊陷阱)：** 若將長網址做 MD5 後截斷前 7 碼，在數十億筆資料下會遇到嚴重的「生日悖論 (Birthday Paradox)」碰撞。處理寫入碰撞（Read-Collision-Retry）會嚴重拖垮資料庫效能。

### C. Security: Non-Enumerable Codes (Feistel Permutation) ✅
- **Problem:** Sequential IDs from the Ticket Server (`0001`, `0002`) are guessable. Competitors can scrape the entire namespace.
- **Solution (L5 亮點)：** 將循序 ID 通過 **Feistel Network** 進行一對一 (Bijection) 數學加密混淆。這不需要網路延遲 (純 CPU 運算)，且能確保短代碼看似隨機，完美防止枚舉攻擊 (Enumeration Attack)。

### D. Advanced L5 Challenge: Database Replication Lag ✅
- **Problem (面試常見情境)：** 用戶寫入 Primary DB 後立刻點擊，但請求被派發到尚未同步的 Read Replica (從庫)，導致 404 找不到網址。
- **Solution:** **Write-Through to Redis**。寫入 DB 時「立刻同步寫入 Redis 並設定短 TTL」。後續立刻發生的讀取都會先命中 Redis 返回 302，這同時完美解決了「讀己之寫 (Read-Your-Writes)」一致性問題與從庫的複製延遲。

---

## 4. Final System Evaluation / 最終評估總結
✅ **Capacity awareness:** Solid sizing on DB (900GB) and Redis Cache (16GB).  
✅ **Latency reduction:** CDN Edge execution eliminates origin load for viral links.  
✅ **Fault tolerance:** Block allocation of IDs prevents ZooKeeper from becoming a write-path bottleneck.  
✅ **Security & Consistency:** Feistel handles enumeration risks, Write-Through handles replication lag.
