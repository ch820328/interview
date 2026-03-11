# System Design: Distributed Web Crawler (架構設計：分散式網頁爬蟲)

**Topic / 主題:** Scalability & Politeness / 可擴展性與禮貌性原則
**Target Level / 目標等級:** Google L4 / L5 (Software Engineer III/IV)
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-11

---

## 1. Requirements & Scale (需求與規模)

### Functional Requirements (功能需求)
**English:**
- **Seed-based Crawling:** Start with a seed list and recursively crawl.
- **Content Storage:** Store HTML and metadata (Title, URL, timestamp).
- **Deduplication:** Mandatory content-level (SimHash) and URL-level deduplication.
- **Politeness:** Respect `robots.txt` and per-domain rate limits.

**中文：**
- **種子爬取：** 從種子清單開始並進行遞迴爬取。
- **內容存儲：** 儲存 HTML 與元數據（標題、URL、時間戳）。
- **去重機制：** 強制的內容級 (SimHash) 與 URL 級去重。
- **禮貌性原則：** 遵守 `robots.txt` 並對各個網域進行頻率限制。

### Non-Functional Requirements (非功能需求)
**English:**
- **Scale:** 1 Billion pages per month (400 QPS average, 1k peak).
- **High Availability:** 99.9% uptime for the Frontier to prevent worker idling.
- **Consistency:** Eventual consistency for storage; higher consistency for state tables.
- **Scalability:** Must handle 60 Billion URLs over 5 years.

**中文：**
- **規模：** 每月 10 億個網頁（平均 400 QPS，峰值 1k）。
- **高可用性：** 排程器需達 99.9% 可用性以避免工作節點閒置。
- **一致性：** 存儲端最終一致性；狀態表端較高一致性。
- **可擴展性：** 需具備處理 5 年內 600 億條 URL 的能力。

---

## 2. Capacity Estimation (容量估算)

| Metric (指標) | Value (數值) | Calculation (計算) |
|---|---|---|
| **QPS (Peak)** | 1,000 req/s | Monthly volume burst handling |
| **Storage (5 Years)** | 6 PB | 1B pages/mo * 100 KB/page * 60 months |
| **URL Seen Index** | 480 GB | 60B URLs * 8 bytes (Hash) |
| **Bloom Filter Mem** | 72 GB | Compressed representation of 60B URLs |

---

## 3. Clarification Q&A (澄清問答情境)

| Question (待澄清問題) | Answer (面試官回覆) |
|---|---|
| **English:** Target data type? | HTML text and metadata only. No media/PDFs. |
| **中文：** 目標數據類型？ | 僅限 HTML 文本與元數據。不抓取多媒體或 PDF。 |
| **English:** Freshness policy? | 30-day base cycle. News sites prioritized. |
| **中文：** 新鮮度政策？ | 30 天基礎週期。新聞網站優先。 |
| **English:** Politeness logic? | One worker per domain queue with delay threshold. |
| **中文：** 禮貌原則邏輯？ | 每個網域隊列同一時間僅限一個 worker 租借，並設有延遲閾值。 |

---

## 4. High-Level Architecture (高階架構圖)

### ASCII Diagram & Component Labels

```text
[ External Seeds ] -> (API Gateway) -> [ URL Frontier (Frontier DB/Bloom) ]
                                             ^               |
                                             |        (Task Lease/Pull)
                                             |               v
[ HTML Storage ] <--- (Fetcher Nodes) <--- (Fetcher Manager / Worker Pool)
      |                     |                        |
      v                     v                        v
[ Metadata DB ] <--- (Content Processor) <--- (HTML Parser / Link Extractor)
                            |
                            +------> (URL Normalizer) ------> [ Back to Frontier ]
```

**English:**
- **Frontier:** The scheduler managing task states (Pending/Leased).
- **Fetcher:** Async node downloading content.
- **Processor:** Link extraction and normalization engine.

**中文：**
- **Frontier (排程器)：** 管理任務狀態（待處理/租用中）的核心排程系統。
- **Fetcher (抓取器)：** 執行內容下載的非同步節點。
- **Processor (處理器)：** 連結提取與正規化引擎。

---

## 5. Request Flows (處理流程)

### Crawl Flow (寫入/爬取流程)
**English:**
1. Fetcher leases batch -> 2. Async DNS resolution -> 3. HTTP Download -> 4. SimHash check -> 5. Extract & Normalize links -> 6. Bloom Filter check -> 7. Push new links to Frontier.

**中文：**
1. 抓取器租借任務 -> 2. 非同步 DNS 解析 -> 3. HTTP 下載 -> 4. SimHash 去重 -> 5. 提取並正規化連結 -> 6. 布隆過濾器檢查 -> 7. 將新連結推回排程器。

---

## 6. Data Model (資料模型)

| Layer (層級) | Choice (選擇) | Reason (原因) |
|---|---|---|
| **Metadata** | HBase / Cassandra | Sharded by URL_Hash; supports heavy write loads. |
| **HTML Blob** | GCS / HDFS | Scalable object storage for Petabyte level. |
| **Bloom Index** | Redis Cluster | Low-latency memory checks for 60B keys. |

---

## 7. Component Interfaces & Mocks (組件介面與 Mock 實作)

### Frontier Lease Interface (gRPC/Proto)
```protobuf
service FrontierService {
  // Worker pulls tasks based on domain availability
  rpc LeaseTasks (LeaseRequest) returns (LeaseResponse);
}

message LeaseRequest {
  string worker_id = 1;
  int32 batch_size = 2; // Optimization: batching
}
```

### Deduplication Service Mock (Python)
```python
class ContentDeduper:
    def is_duplicate(self, content_simhash: int) -> bool:
        # Check against SimHash index in NoSQL
        # Return True if Hamming distance is < threshold
        pass
```

---

## 8. L4+ Depth Analysis: Critical Path (L4+ 深度解析)

| Topic (主題) | L4+ Perspective (L4+ 進階視角) |
|---|---|
| **DNS Optimization** | **English:** Mandatory Async Resolvers. L1 (Worker Local) + L2 (Redis) caching to hide DNS latency. / **中文：** 強制採用非同步解析器。透過 L1 (本地) 與 L2 (Redis) 快取來隱藏 DNS 延遲。 |
| **Adaptive Politeness**| **English:** Use feedback from P99 latency. If target site slows down, Frontier increases delay thresholds dynamically. / **中文：** 根據 P99 延遲進行反饋。若目標主機變慢，排程器自動動態增加延遲。 |
| **Hot Partitioning** | **English:** Shard by `hostname + salt` to distribute load from massive domains (e.g., Wikipedia). / **中文：** 透過 `hostname + salt` 進行分片，以分散大型網域（如維基百科）帶來的後端壓力。 |

---

## 9. Trade-offs (權衡分析)

| Decision (決策) | ✅ Gain (收益) | ❌ Sacrifice (犧牲) |
|---|---|---|
| **Bloom Filter** | Handles 60B keys in 72GB RAM. | Non-zero false positives. |
| **Async Fetch** | High throughput with fewer threads. | Complexity in error handling & timeouts. |

---

## 10. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **URL Frontier** | The core queuing system of a crawler | URL 排程器 |
| **Bloom Filter** | Probabilistic data structure for set membership | 布隆過濾器 |
| **SimHash** | Locality-sensitive hashing for near-duplicates | SimHash |
| **Asynchronous Resolver** | Non-blocking tool for DNS lookups | 非同步解析器 |
