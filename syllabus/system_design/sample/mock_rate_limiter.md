# System Design: Distributed Rate Limiter (架構設計：分散式限流器)

**Topic / 主題:** High-Throughput Traffic Shaping & Global Consistency / 高吞吐量流量治理與全域一致性
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-13

---

## 1. Requirements & Scale (需求與規模)

### Functional Requirements (功能需求)
**English:**
- Support multi-dimensional limiting (UserID, IP, API Key).
- Accurate enforcement for high-value APIs; optimized for low latency in others.
- Fail-open/closed strategies per API metadata.

**中文：**
- 支援多維度限流（UserID, IP, API Key）。
- 對高價值 API 進行精確限流；其餘 API 以低延遲優化為主。
- 根據 API 元數據配置 Fail-open 或 Fail-closed 策略。

### Non-Functional Requirements (非功能需求)
**English:**
- **Scale:** 10M DAU, 1M RPS peak.
- **Latency:** Sub-millisecond response time via SDK-side leasing.
- **Availability:** 99.99% for the limiter service.
- **Consistency:** Eventual consistency for global aggregation; Strong consistency for "Strict Mode".

**中文：**
- **規模：** 1,000 萬日活躍用戶，峰值 100 萬 RPS。
- **延遲：** 透過 SDK 端租約機制達到亞毫秒級響應。
- **可用性：** 限流服務需達 99.99% 可用性。
- **一致性：** 全域彙總採最終一致性；「嚴格模式」採強一致性。

---

## 2. Capacity Estimation (容量估算)

| Metric (指標) | Value (數值) | Calculation (計算) |
|---|---|---|
| **Peak Throughput** | 1,000,000 RPS | Distributed across 10-15 Redis shards per region. |
| **Memory usage** | ~2 GB | 10M users * 64 bytes/entry (Sliding window metadata). |
| **Bandwidth** | 100 MB/s | 1M RPS * 100 bytes (gRPC overhead). |

---

## 3. High-Level Architecture (高階架構圖)

### ASCII Architecture Diagram

```text
[ Global Admin/Config ] -> [ Global Aggregator (GA) ]
                                | (Async Sync)
                                v
+------------------+    +-------------------+
|    NA Region     |    |    APAC Region    |  (Regional Autonomy)
| [Redis Cluster]  |    |  [Redis Cluster]  |
+------------------+    +-------------------+
        ^                        ^
        |                        |
  [ gRPC Service ] <------- [ gRPC Service ]
        ^                        ^
        | (Quota Lease)          |
  [ SDK @ Client Service ] <-----+
```

**English:**
- **SDK:** Implements Quota Leasing and Jittered Early Renewal to reduce backend RPS.
- **Regional Service:** Handles local enforcement using Redis Shards.
- **Global Aggregator:** Periodically (1-5s) rebalances quotas across regions based on consumption.

**中文：**
- **SDK：** 實作配額租借 (Quota Leasing) 與抖動式主動更新，以降低後端負荷。
- **區域服務：** 使用 Redis 分片進行在地化限流判定。
- **全域彙總器 (GA)：** 每 1-5 秒根據各區消耗量動態重新分配配額。

---

## 4. Deep Dive: L5 Scale Challenges (L5 進階剖析)

### Hot Partition Mitigation (熱區問題)
**English:** 
Use **L1 SDK Aggregation** (Batching requests locally for 10ms) and **Virtual Shards** (Splitting a single hot key into $N$ sub-keys) to distribute load across Redis nodes.
**中文：**
使用 **L1 SDK 本地聚合**（在本地緩存 10ms 後批次發送）與 **虛擬分片**（將單一熱門 Key 拆分為 $N$ 個子 Key）來分散 Redis 節點的壓力和熱點。

### Strict Consistency for High-Value APIs (嚴格一致性模式)
**English:** 
Bypass SDK caching, force synchronous gRPC calls, and use Redis Lua scripts for atomic CAS (Check-and-Set) or Spanner for extreme reliability. Adopt Fail-closed strategy.
**中文：**
繞過 SDK 分級快取，強制執行同步 gRPC 呼叫，並使用 Redis Lua 腳本進行原子測試並設定 (CAS)，或使用 Spanner 確保極高可靠性。採用 Fail-closed 策略。

---

## 5. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Quota Leasing** | SDK pulls a batch of tokens for locally autonomous check | 配額租約 / 租借機制 |
| **Thundering Herd** | Many clients renewing leases simultaneously causing backend spikes | 驚群效應 |
| **Fail-open** | Passing requests if the limiter service fails | 故障開放 (放行模式) |
| **Virtual Shard** | Splitting a hot data partition into logical sub-units | 虛擬分片 |
| **Jitter** | Adding randomness to time-based tasks to avoid sync spikes | 隨機抖動 |

---

## 6. Evaluations & Actionable Corrections (評估與改進)

1. **Overall Rating:** **Strong Hire**
2. **Critical Gaps:** 
   - **English:** When discussing Redis, ensure you mention that while Redis is single-threaded for commands, sharding is mandatory for 1M RPS horizontally.
   - **中文：** 討論 Redis 時，須強調雖然單一 Redis 指令是單執行緒，但面對 100 萬 RPS 時，水平擴展的分片架構 (Sharding) 是強制性的。
