# AI 驅動的系統架構 (如 RAG)

### 📌 核心概念
大型語言模型 (LLM) 受限於其訓練資料的截止時間與私有數據的缺乏。RAG (Retrieval-Augmented Generation) 透過「先檢索外部資料庫，再交給 LLM 生成」來解決幻覺 (Hallucination) 與時效性問題。

### 📌 Vector Databases (向量資料庫)
- **概念**：不像傳統關聯式資料庫比對字串，向量庫儲存的是文字轉化為高維度的 Embedding 陣列。
- **核心演算法 (HNSW - Hierarchical Navigable Small World)**：
  - 在高維空間中進行 ANN (Approximate Nearest Neighbor) 搜尋。這是在查詢延遲 (Latency) 與準確率 (Recall) 之間的極致 Trade-off。
- **適用情境**：語意相似度檢索（例如：搜尋「蘋果手機」也能跑出「iPhone 15」，因為它們在向量空間裡的距離很近）、以圖搜圖。

### 📌 Embeddings (嵌入/向量化)
- **概念**：將非結構化數據 (文本、圖像、影片) 壓縮成長度固定的浮點數陣列。
- **系統設計挑戰**：
  - 如何即時地、非同步地把海量公司私有文件打成 Embeddings 並寫入向量資料庫？
  - **解法**：在設計系統時，通常需要實作一個完整的 Data Pipeline，利用 Message Queue (Pub/Sub) 去觸發 Worker 節點呼叫 Embedding API，再 Batch 寫入 VectorDB 以降低 API 開銷。
