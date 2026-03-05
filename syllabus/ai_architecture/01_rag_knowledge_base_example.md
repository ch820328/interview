# 實戰範例：設計企業內部知識庫問答系統 (RAG Architecture)

### 🗣️ 面試題目
**"Design an Internal Company Knowledge Base Q&A System" (設計一個企業內部的知識庫問答系統)**

**Background:**
公司內部有數百萬計的文件（Markdown, PDFs, Google Docs）。當工程師要找設計文件或 Code 規範時，傳統關鍵字搜尋效果差。希望設計一個基於 LLM 的 Chatbot，當工程師發問時，系統能擷取相關內部文件，並統整出一份完整的回答。

**Constraints:**
1. 不能把全公司文件一次性丟進 Prompt（Token 受限且昂貴）。
2. LLM Inference 時間極長（10~30 秒）。
3. 內部文件每天都會有上萬篇的新增或修改。

---

### 🌟 高階系統設計 (High-Level Design) 藍圖

為了解決這個問題，業界標準做法是採用 **RAG (Retrieval-Augmented Generation / 檢索增強生成)** 架構。
整個系統可以拆分為兩條獨立的 Pipeline：

#### 1. 資料寫入管線 (Offline Data Ingestion Pipeline)
這條管線負責處理每天新增/修改的上萬篇文件，將其轉換為可供檢索的格式。

*   **Crawler / Trigger Worker**: 透過 Webhook 或 Cron Job 定期抓取新的文件變更。
*   **Message Queue (Kafka / PubSub)**: **(L4 亮點)** 用於解耦系統。抓取到變更事件後送入 Queue，避免瞬間流量壓垮後續的 Embedding API。
*   **Chunking (切塊處理)**: 將長篇文章切割成固定大小的語意段落 (Chunks)，例如每 500 字落為一個單位。
*   **Embedding Model**: 呼叫外部或地端部署的模型 (如 OpenAI `text-embedding-ada-002`)，將這些段落文字轉化為高維度的「浮點數陣列 (Vector)」。
*   **Vector Database (向量資料庫)**: 將 Vector 帶上 Metadata (如文章 URL) 存入專門的資料庫 (如 Pinecone, Milvus, Qdrant)。

#### 2. 使用者發問管線 (Online Query Pipeline - RAG)
當 User 在前端輸入問題（例如：「如何部署微服務到 Staging？」），系統的即時回應流程：

*   **User Embeddings**: Backend 接收到 Request 後，將 User 的問題字串同樣打去 Embedding API 轉成 Vector。
*   **Similarity Search (相似度搜尋)**: 拿這個 Vector 去 **VectorDB** 內進行最近鄰居搜尋 (ANN - Approximate Nearest Neighbor)，找出語意上最接近的 Top-5 相關段落。
*   **Prompt Construction**: Backend 將這 5 個段落組合進 Prompt 中，作為背景知識 (Context)。
    *   *Prompt 範例：「你是一個工程師助手。**根據以下背景資料**，請回答問題：『如何部署微服務到 Staging？』。**若資料中無相關解答，請回答不知道。**」*
*   **LLM Generation**: 將整包 Prompt 發送給 LLM 進行生成計算。

#### 3. 使用者體驗與網路協定優化 (UX & Latency Handling)
*   **Streaming API (SSE / WebSocket)**: **(L4 核心亮點)**
    為了解決 LLM 需耗時 10~30 秒生成的極差體驗，Backend 必須採用 **Server-Sent Events (SSE)** 協定。當 LLM 在背後每生成一個 Token (單字) 時，Backend 就立刻將該字元推送到 Frontend。
    這能讓使用者在按下送出後的 0.5 秒內就看到第一個字如打字機般湧現 (Streaming)，極大地提升 UX。

---

### 💡 面試官點評總結
在 Modern AI Architecture 面試中，掌握此題的三大核心關鍵字即可拿下高分：
1.  **RAG**: 解決 LLM 缺乏私有資料庫與幻覺 (Hallucination) 的唯一正解。
2.  **Vector Database**: 實現語意搜尋 (Semantic Search) 而非單純關鍵字比對的利器。
3.  **SSE (Streaming)**: 解決 AI 應用天生高延遲 (High Latency) 瓶頸的標準網路協定設計。
