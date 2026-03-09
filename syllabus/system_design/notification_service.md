# System Design Interview: Notification Service (通知服務系統設計)

**Topic / 主題:** Notification Service — Multi-channel, High-throughput
**Target Level / 目標等級:** Google L4 / L5
**Session Rating / 場次評分:** **Strong Hire**
**Session Date / 面試日期:** 2026-03-09

---

## 1. Requirements Gathering (需求澄清)

### Functional Requirements (功能需求)
**English:**
- Send notifications to users via Push, Email, SMS (extensible to WhatsApp)
- Support transactional (OTP) and marketing (bulk) notification types
- Provide delivery status tracking per notification

**中文:**
- 透過推播、電子郵件、SMS 發送通知（可擴展至 WhatsApp）
- 支援交易型（OTP）與行銷型（大量）通知
- 提供每則通知的送達狀態追蹤

### Non-Functional Requirements (非功能需求)
**English:**
- **Transactional SLA:** Deliver OTPs within 1 second
- **At-least-once delivery** with idempotency (no duplicate sends on retry)
- **Extensibility:** New providers addable without core logic changes
- **Scale:** 200M DAU, ~1B notifications/day, 50k peak QPS

**中文:**
- **交易型 SLA：** OTP 必須在 1 秒內送達
- **至少一次送達**，並具備冪等性（重試不會重複發送）
- **可擴展性：** 增加新供應商不需修改核心邏輯
- **規模：** 2 億 DAU，每日約 10 億則通知，峰值 5 萬 QPS

---

## 2. Capacity Estimation (容量估算)

| Metric (指標) | Calculation (計算) | Result (結果) |
|---|---|---|
| Avg Write QPS | 10^9 / 86,400 | ~11,574 QPS |
| Peak Write QPS | Given | 50,000 QPS |
| Burst Ratio | 50k / 11.5k | ~4–5× |
| Storage/record | metadata + template + status | ~500 bytes |
| Daily storage | 10^9 × 500B | 500 GB/day |
| 1-year retention | 500 GB × 365 | ~182 TB |
| Peak ingress BW | 50k × 500B | 25 MB/s |

**Key Engineering Conclusions (工程結論):**
1. Async queue is mandatory — 1s OTP SLA cannot tolerate synchronous provider calls
2. Single-node DB is dead at 500 GB/day — horizontal sharding required from day one
3. External provider egress (Twilio, FCM) is the real bottleneck, not internal ingress

---

## 3. API Design (API 設計)

### Auth & Trust Boundary (認證與信任邊界)
**English:** mTLS via Service Mesh (Istio/Envoy) for authentication. JWT-based RBAC for authorization — scoped tokens prevent Marketing Service from triggering System Critical notifications.

**中文:** 使用 Service Mesh 實施 mTLS 認證。JWT RBAC 授權——具作用域的 Token 防止行銷服務誤觸系統關鍵通知。

### Core API (核心 API)

**POST /v1/notifications**
```json
// Request
{
  "request_id": "uuid-v4",           // idempotency key
  "user_id": "user_12345",
  "priority": "HIGH",                // HIGH → 1s queue | LOW → batch queue
  "template_id": "otp_template_v1",
  "template_params": { "code": "123456", "expiry": "5 mins" },
  "preferred_channels": ["PUSH", "SMS"],
  "created_at": "2026-03-09T17:00:00Z",  // for TTL/staleness check
  "ttl_seconds": 120,
  "callback_url": "https://order-service.com/webhook"
}

// Response: 202 Accepted
{
  "status": "accepted",
  "request_id": "uuid-v4",
  "estimated_delivery": "2026-03-09T17:00:01Z"
}
```

**GET /v1/notifications/{request_id}**
Returns: `PENDING | SENT | DELIVERED | FAILED`

### Provider Interface (Provider 介面)
```python
class NotificationProvider(ABC):
    @abstractmethod
    def send(self, user_contact: str, content: str, metadata: dict) -> ProviderResponse:
        """
        Standardizes calls to external vendors (Twilio, FCM, SendGrid, WhatsApp).
        Each adapter encapsulates vendor-specific error mapping and circuit breaker logic.
        每個 Adapter 封裝供應商的錯誤對應與熔斷器邏輯。
        """
        pass
```

---

## 4. High-Level Architecture (高階架構)

```
External Services          Internal Services            Storage
──────────────            ─────────────────            ───────
Client Services   ──▶  [L7 Load Balancer]
                              │
                    [API Service / Gatekeeper]  ──▶  [Redis]
                    - mTLS + RBAC auth                (idempotency keys,
                    - SETNX idempotency check          user prefs, templates)
                    - Rate limiting
                    - 202 Accepted response
                              │
                     ┌────────┴────────┐
                [Kafka: HIGH_PRIORITY] [Kafka: LOW_PRIORITY]
                     │                        │
            ┌────────┴────────┐       [Batch Workers]
            │                 │
       [Push Workers]   [SMS Workers]   [Email Workers]
       (channel-isolated clusters for fault isolation)
            │
     [Provider Adapters]  ──▶  FCM / Twilio / SendGrid / WhatsApp
            │
     ┌──────┴──────┐
 [Notification   [DLQ]
  Log DB]            │
 (Cassandra/     [Reconciliation
  Bigtable)       Service]
```

### Component Justification (組件設計理由)

| Component (組件) | Why It Exists (存在理由) |
|---|---|
| **L7 Load Balancer** | TLS termination, traffic distribution / TLS 終止、流量分發 |
| **Kafka (2 topics)** | Buffer 50k QPS; priority isolation prevents OTP starvation by bulk mail / 緩衝峰值；優先級隔離防止 OTP 被行銷訊息飢餓 |
| **Channel-isolated Worker clusters** | Fault isolation: Twilio slowness only backs up SMS queue, not Push / 故障隔離：Twilio 變慢只影響 SMS 佇列 |
| **Redis** | Idempotency key store (SETNX); hot template + user preference cache / 冪等性金鑰；熱點模板與用戶偏好快取 |
| **Cassandra/Bigtable** | Sequential write optimization for 50k QPS notification logs / 順序寫入優化，適合高 QPS 日誌 |
| **DLQ** | Captures permanently failed messages for replay or inspection / 捕捉永久失敗訊息以供重放或檢查 |
| **Reconciliation Service** | Owns DLQ re-drive logic; can switch providers before replaying / 擁有 DLQ 重放職責；可在重放前切換供應商 |

---

## 5. Deep Dive: Idempotency Race Condition (冪等性競態條件)

**Problem:** Two API replicas receive the same `request_id` simultaneously, both get Redis cache miss, both publish to Kafka. User gets two OTPs.

**問題：** 兩個 API replica 同時收到相同 `request_id`，同時 Redis cache miss，同時發到 Kafka。用戶收到兩則 OTP。

**Solution — Defense in Depth (多層防禦):**

**Layer 1 — Redis SETNX (API Layer):**
```python
# Atomic operation: SET if Not eXists + TTL
result = redis.set(request_id, "processing", nx=True, px=10000)
if not result:
    return existing_response(request_id)  # duplicate detected
```
Redis is single-threaded — two concurrent commands are always serialized.
Redis 是單執行緒——兩個並發指令必有先後，天然原子。

**Layer 2 — DB Unique Constraint (Worker Layer):**
```python
# Before calling external provider (irreversible action)
try:
    db.insert(request_id=msg.request_id, status="PROCESSING")
except UniqueConstraintError:
    return  # another worker already handling this
```
This is the last-resort gate before the irreversible external API call.
這是在不可逆的外部 API 呼叫前的最後一道攔截。

---

## 6. Deep Dive: Provider Failure & Backlog (供應商故障與積壓)

### Retry Strategy (重試策略)
```python
wait = base * (2 ** attempt) + random.uniform(0, jitter)
# Max 3-5 retries to prevent head-of-line blocking
```
Exponential backoff with jitter prevents Thundering Herd on provider recovery.
指數退避加隨機抖動防止供應商恢復時的驚群效應。

### DLQ Re-drive (DLQ 重放)
- After max retries: message moves to DLQ
- Reconciliation Service monitors DLQ, can switch `ProviderAdapter` (e.g., Twilio → MessageBird) before re-driving
- 達到最大重試次數後進入 DLQ；對帳服務可切換供應商後重放

### Staleness Check for OTP Expiry (OTP 過期短路)
```python
# At Worker, BEFORE calling external provider
if (current_time - msg.created_at).seconds > msg.ttl_seconds:
    log_drop(reason="EXPIRED", request_id=msg.request_id)
    return  # skip provider call entirely
```
When Twilio recovers after 30-min outage, workers drain expired OTPs instantly without wasting API calls, unblocking fresh valid messages.

Twilio 恢復後，Worker 不呼叫 API 直接丟棄過期 OTP，快速排空積壓，讓新訊息更早送達。

### Load Shedding: Kafka Offset Skip (負載卸載)
If lag threatens real-time OTP delivery: temporarily advance consumer offset, process backlog via separate batch job post-recovery.

積壓嚴重威脅即時 OTP 時：暫時跳過 Consumer Offset，由獨立批次作業在故障後分析處理。

---

## 7. Full Evaluation Rubric (完整評估表)

| Dimension / 維度 | Rating / 評分 | Notes / 備註 |
|---|---|---|
| **Overall / 總評** | **Strong Hire** | Deep operational thinking throughout |
| **Requirements / 需求澄清** | ✅ L5 | Priority split, idempotency, extensibility all named upfront |
| **Estimation / 容量估算** | ✅ Strong | Correct math + right engineering conclusions |
| **API Design / API 設計** | ✅ L5 | mTLS, RBAC, 202 Async, Provider abstraction |
| **Architecture / 架構** | ✅ Strong | Fault isolation, Queue priority, DLQ path all correct |
| **Idempotency / 冪等性** | ✅ L5 | SETNX + DB unique constraint Defense in Depth |
| **Failure Handling / 故障處理** | ✅ L5+ | Staleness check + Kafka offset skip = rare insight |
| **Data Model / 資料模型** | ❌ Gap | Partition key and schema never defined |
| **Kafka Durability / Kafka 持久性** | ❌ Gap | replication.factor / min.insync.replicas not mentioned |
| **User Preference Routing / 用戶偏好路由** | ⚠️ Gap | Checked but position in flow unclear |

---

## 8. Actionable Corrections (改進建議)

**English:**
1. **Always define data model explicitly.** For Cassandra: state partition key + sort key + primary query pattern. *"Partition by `user_id`, sort by `notification_id` DESC for 'show latest notifications for user X.'"*
2. **Kafka durability is non-negotiable.** Always state: `replication.factor=3`, `min.insync.replicas=2`.
3. **Show user preference check in the flow.** Name the exact component — at API ingestion (to skip Kafka publish entirely) or at Worker pre-dispatch.

**中文:**
1. **永遠明確定義資料模型。** 對 Cassandra 需說明 Partition Key、Sort Key 與主要查詢模式。
2. **Kafka 持久性不可省略。** 必須說明 `replication.factor=3`、`min.insync.replicas=2`。
3. **在架構流程中標示用戶偏好檢查的位置。** 是在 API 層（防止進入 Kafka）還是在 Worker 層（發送前）？

---

## 9. Technical Term Dictionary (技術名詞字典)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| **Idempotency** | A property where repeated identical operations produce the same result | 冪等性：相同操作重複執行結果不變 |
| **SETNX** | Redis atomic "SET if Not eXists" operation | Redis 原子操作：「若不存在則設定」 |
| **Thundering Herd** | A scenario where many processes wake simultaneously and overload a resource | 驚群效應：大量程序同時喚醒並擠垮共享資源 |
| **Exponential Backoff with Jitter** | Retry strategy with exponentially increasing wait + randomness to prevent synchronized retries | 指數退避加隨機抖動：防止重試同步化的策略 |
| **Dead Letter Queue (DLQ)** | A queue for messages that failed all retry attempts | 死信佇列：存放已耗盡所有重試次數的失敗訊息 |
| **Circuit Breaker** | A pattern that stops sending requests to a failing service to allow recovery | 熔斷器：停止向故障服務發送請求以讓其恢復 |
| **mTLS** | Mutual TLS — both client and server authenticate each other | 雙向 TLS：客戶端與伺服器互相驗證身份 |
| **Head-of-line Blocking** | Slower messages at the front of a queue block all messages behind them | 隊首阻塞：佇列前端的慢速訊息阻塞後方所有訊息 |
| **Defense in Depth** | Multiple independent security/reliability layers so no single failure causes a breach | 縱深防禦：多層獨立防護，確保單點失效不造成漏洞 |
| **Staleness Check** | Verifying that a message has not expired before processing it | 過期性檢查：在處理訊息前確認其尚未逾期 |
| **Adapter Pattern** | A design pattern that translates one interface into another for compatibility | 適配器模式：將一個介面轉換為另一個以達到相容性 |
| **replication.factor** | Kafka config: number of copies of each partition across brokers | Kafka 配置：每個分區在不同 Broker 上的副本數量 |
| **min.insync.replicas** | Kafka config: minimum replicas that must acknowledge a write before it succeeds | Kafka 配置：寫入成功前必須確認的最小副本數量 |
