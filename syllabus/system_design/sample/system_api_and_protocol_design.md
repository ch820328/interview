# API 與通訊協定設計 (API & Protocols)

### 📌 核心概念
客戶端如何與伺服器溝通，或是微服務之間的相互調用。

### 📌 Trade-offs 與適用情境
- **RESTful API (JSON over HTTP/1.1)**:
  - **優點**：通用性極高、支援所有語言與瀏覽器、可緩存 (HTTP Caching)。
  - **缺點**：JSON 體積龐大不省頻寬、基於文字解析較慢。
  - **適用**：公開對外的 Public API、前端網頁串接。
- **gRPC (Protocol Buffers over HTTP/2)**:
  - **優點**：序列化體積小速度快、原生支援雙向 Streaming、強型別 (Strongly Typed Schema)。
  - **缺點**：瀏覽器支援度差（需透過 gRPC-Web proxy）、不好 Debug (因為是 Binary格式)。
  - **適用**：內部微服務之前的快速溝通、低延遲要求的場景。
- **WebSocket / Server-Sent Events (SSE)**:
  - **優點**：真正的全雙工/半雙工即時通訊，免除 Polling 開銷。
  - **適用**：聊天室、即時股票報價、協作編輯 (如 Google Docs)。
