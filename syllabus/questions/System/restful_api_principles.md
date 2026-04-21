# RESTful API: Architectural Principles (RESTful API：架構原則深度分析)

## I. Problem Statement & Nuances (題目與細節)
What defines a "Truly RESTful" API? Explain the difference between REST and RPC, and the importance of **Idempotency** in distributed systems.
什麼定義了「真正的 RESTful」API？請解釋 REST 與 RPC 的區別，以及分布式系統中「等冪性 (Idempotency)」的重要性。

**Nucleus Insights (核心觀點):**
- **Resource Oriented**: In REST, everything is a **Resource** (Noun), not an action (Verb). (以「資源」為中心，而非「動作」。)
- **Representational State Transfer**: The client and server exchange *representations* of resources (JSON/XML) to transition the application state. (透過交換資源表示形式來轉換應用程式狀態。)
- **HATEOAS**: Hypermedia as the Engine of Application State—the idea that the API response should contain links to the next possible actions. (API 回傳應包含下一步動作的連結。)

---

## II. Mechanical Deep-Dive: HTTP Verbs & Idempotency (底層原理：動詞與等冪性)

**Idempotency (等冪性)** means that making the same request multiple times has the same effect as a single request.
「等冪性」是指多次執行相同請求產生的效果與單次請求相同。

| Verb | Intent (意圖) | Idempotent? | Safe? |
|---|---|---|---|
| **GET** | Retrieve a resource. | **Yes** | **Yes** |
| **POST**| Create a resource. | **No** | **No** |
| **PUT** | Replace a resource. | **Yes** | **No** |
| **PATCH**| Update a resource. | **No** (Depends)| **No** |
| **DELETE**| Remove a resource. | **Yes** | **No** |

*Expert Note: DELETE is idempotent because removing a non-existent resource results in the same final state (gone) as the first time.*

---

## III. Quantitative Analysis: Versioning Strategies (量化指標與對比)

| Strategy | Example | Pros (優點) | Cons (缺點) |
|---|---|---|---|
| **URL Path** | `/v1/users` | Visible, easy to cache. | Pollutes the URL space. |
| **Headers** | `Accept: version=2` | Clean URLs. | Harder to test in browsers. |
| **Domain** | `v2.api.com` | DNS level routing. | SSL/CORS complexity. |

---

## IV. Professional API Best Practices (專業 API 實踐)

| Rule | Explanation (說明) |
|---|---|
| **Plural Nouns** | Use `/users`, not `/getUser`. (使用複數名詞。) |
| **Statelessness** | Server stores NO client state; each request is self-contained. (伺服器不儲存客戶端狀態。) |
| **Paging/Filtering** | Use Query Params: `/users?page=1&limit=10`. (使用查詢參數進行分頁。) |
| **Appropriate Codes** | `201` for Created, `409` for Conflict, `429` for Rate Limit. |

---

## V. Beyond REST: The RPC Comparison (對比 RPC)

**REST vs. gRPC (The Modern Debate):**
- **REST**: Uses Text (JSON), Human-readable, browser-friendly, $O(\text{Parsing Overhead})$.
- **gRPC**: Uses Binary (Protobuf), $O(1)$ serialization, Schema-defined (Protoc), best for performance intra-service.

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **The PUT vs PATCH Trap**: Using `PUT` for partial updates can lead to data loss if fields are missed. (PUT 用於全量替換，局部更新應使用 PATCH。)
2. **Missing Rate Limiting**: REST APIs are vulnerable to DoS if they don't return `429 Too Many Requests` with `Retry-After` headers. (缺乏限流會導致服務崩潰。)
3. **N+1 Query Problem**: Poorly designed REST endpoints can force the client to make multiple calls (e.g., `/users` then `/users/1/orders`). **Solution**: Side-loading or GraphQL. (導致客戶端發出過多請求。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| HATEOAS | 應用程式狀態引擎 | Providing links in API responses for discoery. (在回傳中提供連結引導行為。) |
| Statelessness | 無狀態性 | Every request is complete without needing previous context. (每個請求都在無前文提示下完成。) |
| Resource | 資源 | An entity that is the primary focus of the API. (API 的核心實體。) |
| Idempotency | 等冪性 | Ensuring a re-sent request doesn't cause dual updates. (確保重送請求不會造成重複更新。) |
