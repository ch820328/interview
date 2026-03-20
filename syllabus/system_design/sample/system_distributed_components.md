# 分散式系統元件 (核心積木)

### 📌 Load Balancer (負載平衡器)
- **概念**：將龐大流量均勻分配給後端的多台 Server。
- **Trade-offs**：
  - **L4 LB (Network Layer)**：速度極快，但不看 HTTP 內容。
  - **L7 LB (Application Layer)**：可以針對 URL、Cookie 進行路由，但需要解析 HTTP，稍微耗能。
- **Algorithms**：Round-Robin, Least Connections, Consistent Hashing (非常重要，用於 Server 節點增減時減少 Cache Miss)。

### 📌 Caching Strategies (快取策略)
- **概念**：將熱點資料存在記憶體 (如 Redis/Memcached) 減少 DB 壓力。
- **Trade-offs**：
  - **Write-around**：直接寫入 DB 不更新 Cache，適合寫入多讀取少的資料。
  - **Write-through**：同時寫入 Cache 和 DB，延遲較高但保證強一致性。
  - **Write-back (Write-behind)**：只寫入 Cache 即回傳成功，非同步寫入 DB。效能極佳，但如果機器重啟會遺失資料。
- **Google 面試必考地雷**：如何處理 Cache Stampede (緩存擊穿) 以及 Cache Avalanche (緩存雪崩)？

### 📌 Message Queues (訊息佇列)
- **概念**：非同步處理任務、系統解耦、削峰填谷 (Peak Shaving)。
- **Trade-offs**：
  - **RabbitMQ (AMQP)**：著重路由規則、保證送達、低延遲（適合訂單系統）。
  - **Kafka / Google Pub/Sub**：超高吞吐量、訊息持久化、適合海量 Logs 與 Event Sourcing (事件回溯)。
- **L4 深潛問題**：若 Consumer 處理速度跟不上導致 Queue 堆積怎麼辦？如何保證 Exactly-Once Delivery (精確一次送達)？
