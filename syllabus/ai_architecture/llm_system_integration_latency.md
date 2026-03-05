# 系統整合與部署考量 (System Integration & Deployment)

### 📌 處理 LLM Inference 的高延遲 (Latency)
- **問題**：跟 LLM API 溝通往往需要數秒到數十秒，這完全打破了傳統 Web API 要求的 200ms 以內回應時間。
- **解法 (系統架構層級)**：
  - **Streaming API (Server-Sent Events / WebSocket)**：讓 LLM 一個字一個字吐回前端，極大化提升使用者的 UX。
  - **非同步 Queue 架構**：如果是在背景產圖、產長文，應該讓 API 立刻回傳 `202 Accepted` 與一個 `Job ID`，背景利用 Celery / PubSub 處理完後，前端再用 Polling 或 WebSocket 拿結果。
  - **Semantic Caching (語意快取)**：如果使用者問了很類似的問題，利用 Redis 等技術結合 Vector Search，如果不進 LLM 直接把上次算好的答案丟回。

### 📌 微服務架構下的模組拆分 (Microservices Boundary)
- 遇到 AI 專案時，不應把它全部寫在一支單體應用 (Monolith) 裡面。
- **拆分建議 (L4 面試的亮點)**：
  - **Crawling Service (資料爬取服務)**：獨立拉出，這層最容易被 Ban、需要管理 Proxy 和 Retry。
  - **Vectorization Worker (向量化運算池)**：CPU/GPU 密集型服務，隨 Queue 的長度動態 Auto-Scaling。
  - **Chat/QA Service (問答前端 API)**：負責串接 LLM，高併發的 I/O 密集型 Node.js 或 Go Server，專門處理 SSE Streaming 回傳給 Client 網域。

### 📌 故障處理 (Failure Modes) 與 成本控管 (Cost Optimization)
- 如果 OpenAI / Gemini API 忽然掛掉 (HTTP 502) 怎麼辦？
  - **Circuit Breaker (斷路器)**：避免一直接續引發自身系統耗盡 Thread 資源。
  - **Fallback Mechanisms**：從商業邏輯定義，當 LLM 無法工作時，系統能不能退化成「傳統搜尋」回給 User？
- **速率限制方案 (Rate Limiting on Prompt Tokens)**：設計系統去紀錄並限制每個 User 每分鐘消耗的 Token 數量，保護公司不破產。
