# Google System Design Syllabus — Chat System (1-on-1)
# Google 系統設計面試指南 — 聊天系統（一對一）

## 1. Requirements & Scale / 系統需求與規模

**English:**
- **Functional:** 1-on-1 text messaging, online/offline status. No read receipts or group chats. Messages delivered in real-time when online, stored and delivered later when offline. Max 1000 characters per message.
- **Non-Functional:** Low latency (P99 < 200ms), High Availability (99.99%), At-least-once delivery, Causal Consistency.
- **Scale Math:** 
  - DAU: 100 Million
  - Concurrent Connections (CCU): 30 Million
  - Writes: 5 Billion messages/day $\approx$ 290,000 Peak QPS
  - Storage: 750 GB/day (150 Bytes per message). 5-Year Storage $\approx$ 1.4 PB.

**Chinese (Traditional):**
- **功能性需求：** 一對一純文字訊息，支援在線/離線狀態。不包含已讀回執或群組聊天。在線時即時傳遞，離線時儲存並在重新上線時送達。每則訊息最多 1000 字元。
- **非功能性需求：** 低延遲 (P99 < 200ms)、高可用性 (99.99%)、至少一次交付 (At-least-once)、因果一致性 (Causal Consistency)。
- **系統規模與估算：**
  - DAU (日活躍用戶)：1 億
  - 並發連線數 (CCU)：3000 萬
  - 寫入量：每日 50 億則訊息 $\approx$ 尖峰 290,000 QPS
  - 存儲容量：每日 750 GB（每則 150 Bytes）。5 年存儲 $\approx$ 1.4 PB。

## 2. Clarification Q&A / 澄清與問答

| Question (EN) | Answer (EN) | Question (ZH) | Answer (ZH) |
|-------------|-------------|-------------|-------------|
| Read receipts and group chats? | No, out of scope for 45 mins. | 需要已讀回執和群組聊天嗎？ | 不需要，在 45 分鐘內超出範圍。 |
| Message encryption? | Standard TLS is fine. No E2EE needed. | 需要訊息加密嗎？ | 標準 TLS 即可，不需端到端加密 (E2EE)。 |
| Offline delivery mechanism? | Store offline; deliver when the user reconnects. | 離線傳遞機制為何？ | 離線時儲存，用戶重新連線時傳遞。 |

## 3. Architecture Diagram / 架構圖

```text
User A (Sender)                               User B (Receiver)
      |                                              |
      v                                              v
[API Gateway]                                  [Push Service] (FCM/APNs) - for offline wake-up
      |                                              ^
      v                                              |
[Connection Service] (WebSocket Servers: Manage 30M CCU)
      |         \
      |          \____> [Connection Registry] (Redis: User_ID -> Server_ID mapping)
      v          
[Message Queue] (Kafka: Decouple high write throughput)
      |
      v
[Message Service] (Handles sequencing, offline queries, push trigger)
      |
      v
[NoSQL Database] (ScyllaDB / Cassandra: Persistent Storage)
```

## 4. Write + Read Request Flows / 讀寫請求流程

**English (Message Sending Flow):**
1. User A sends a message via WebSocket to `Server_A`.
2. `Server_A` generates a Snowflake ID and asynchronously pushes the message to Kafka for DB persistence.
3. `Server_A` checks the Redis Registry. If User B is online on `Server_B`, `Server_A` forwards the message via RPC to `Server_B`.
4. `Server_B` pushes the message down the WebSocket to User B.
5. If User B is offline, the Message Service triggers a background task to APNs/FCM to send a Push Notification.

**Chinese (Traditional) (發送訊息流程):**
1. User A 透過 WebSocket 將訊息發送給 `Server_A`。
2. `Server_A` 產生 Snowflake ID，並非同步將訊息放入 Kafka 以寫入資料庫。
3. `Server_A` 查詢 Redis 註冊表。若 User B 正在線並連接於 `Server_B`，`Server_A` 會透過 RPC 轉發訊息給 `Server_B`。
4. `Server_B` 透過 WebSocket 推播訊息給 User B。
5. 若 User B 離線，Message Service 會觸發背景任務，透過 APNs/FCM 發送推播通知。

## 5. Trade-offs & Deep Dives / 權衡與深度分析

| Decision (決策) | ✅ Gain (優勢) | ❌ Sacrifice / Risk (犧牲 / 風險) |
|---------------|--------------|---------------------------------|
| **Protocol: WebSocket vs HTTP Polling** | Real-time, low latency, avoids high HTTP header overhead for 30M connections. (即時、低延遲、避免 3000 萬連線的 HTTP 標頭開銷。) | Stateful architecture requires connection routing and complicates load balancing. (有狀態架構需要連線路由，增加負載平衡的複雜度。) |
| **Deduplication: Client-Side filtering** | Offloads work to edges, naturally handles network dropped ACKs. (將工作負載卸載至客戶端，自然處理網路 ACK 遺失問題。) | Clients must maintain local DB indices and logic natively. (客戶端必須自行維護本地資料庫索引與邏輯。) |
| **Partition Key: `(Conversation_ID, Time_Bucket)` instead of just `Conversation_ID`** | Prevents Cassandra Super Partitions & OOM crashes on multi-year chat histories. (防止 Cassandra 因多年聊天紀錄產生超級分區並導致記憶體溢出。) | Queries spanning multiple months require fetching across multiple nodes. (跨越多個月的查詢需要向多個節點抓取資料。) |

## 6. Full Evaluation Rubric / 完整評估表

**English:**
- **Overall Rating:** Strong Hire
- **Architecture & Design:** Excellent separation of concerns. Dedicating the Connection Registry (Redis) away from the Async Write Queue (Kafka) and Persistent Store (ScyllaDB) shows highly mature L4+ architectural design.
- **Analytical Depth:** Masterful handling of bottlenecks. Moving deduplication to the client-side and fixing the Cassandra Super Partition problem by applying time-bucketing shows deep operational experience.
- **Actionable Corrections:** No major flaws. Continue driving capacity math and bottleneck deep dives proactively.

**Chinese (Traditional):**
- **綜合評分：** 強烈建議錄取 (Strong Hire)
- **架構與設計：** 極佳的關注點分離。將連線註冊表 (Redis)、非同步寫入佇列 (Kafka) 與持久化儲存 (ScyllaDB) 獨立開來，展現了高度成熟的 L4+ 架構設計能力。
- **分析深度：** 完美解決系統瓶頸。將去重邏輯移至客戶端，並透過「時間分桶 (Time-Bucketing)」解決 Cassandra 超級分區問題，證明了深厚的維運與資料建模經驗。
- **可執行的改進建議：** 無重大缺失。請保持這種主動推進容量估算與瓶頸分析的節奏。

---

## 7. Technical Term Dictionary (Appendix) / 技術名詞字典 (附錄)

**English:**
- **WebSocket:** A computer communications protocol, providing full-duplex communication channels over a single TCP connection. Perfect for real-time chat.
- **Kafka:** A distributed event streaming platform used for high-performance data pipelines and decoupling heavy write workloads from databases.
- **Cassandra / ScyllaDB:** A highly scalable, distributed NoSQL database designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure. Excellent for heavy write workloads.
- **Snowflake ID:** A 64-bit globally unique identifier system created by Twitter, generating IDs that are roughly time-sortable.
- **Super Partition:** A massive data partition in NoSQL databases like Cassandra that occurs when too much data shares the same Partition Key, leading to memory and performance crashes.
- **Time-Bucketing:** A data modeling technique where timestamps (like Year-Month) are appended to a Partition Key to forcibly break apart a Super Partition into smaller, manageable chunks.
- **FCM / APNs:** Firebase Cloud Messaging (Google) and Apple Push Notification service. Third-party services required to wake up out-of-focus or backgrounded mobile apps.

**Chinese (Traditional):**
- **WebSocket：** 一種電腦通訊協定，在單一 TCP 連線上提供全雙工通訊管道，非常適合即時聊天系統。
- **Kafka：** 分散式事件流平台，用於高效能資料管道，並能有效將高併發寫入負載從資料庫解耦。
- **Cassandra / ScyllaDB：** 高度可擴展的分散式 NoSQL 資料庫，專為跨多台伺服器處理巨量資料而設計，提供高可用性且無單點故障。非常適合高寫入負載 (Write-Heavy)。
- **Snowflake ID (雪花演算法)：** 由 Twitter 開發的 64-bit 全域唯一識別碼產生系統，其產生的 ID 具有大致按時間排序的特性。
- **Super Partition (超級分區)：** 當 NoSQL 資料庫中過多資料共用同一個 Partition Key 時所產生的巨大資料塊，會導致記憶體耗盡與效能崩潰。
- **Time-Bucketing (時間分桶)：** 一種資料建模技術，將時間戳記 (例如年月) 附加到 Partition Key 上，強制將超級分區拆解成眾多小巧、易管理的分塊。
- **FCM / APNs：** 讓背景或離線的行動應用程式被喚醒並接收推送通知的第三方服務（Firebase 與蘋果推播服務）。
