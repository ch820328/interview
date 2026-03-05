# 經典架構面試題解析

這裡列出 L4 System Design 最常被考到的經典架構與其技術亮點：

- **Design a Rate Limiter (API 限流器)**：
  - **重點考驗**：演算法選擇 (Token Bucket vs Leaky Bucket vs Fixed/Sliding Window)、如何用 Redis 實作分散式限流鎖。
- **Design a Key-Value Store (分散式快取系統)**：
  - **重點考驗**：Consistent Hashing、Data Replication Protocol (如 Raft/Paxos 或是 Dynamo-style Quorum based: W + R > N)、Gossip Protocol。
- **Design a Distributed Message Queue (仿 Kafka)**：
  - **重點考驗**：如何利用磁碟 Sequential IO 進行極致的寫入優化、Consumer Group 的 Offset 管理 (ZooKeeper/MetaDB)。
