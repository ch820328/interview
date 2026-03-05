# 資料庫與儲存 (Storage & Databases)

### 📌 SQL vs. NoSQL
- **SQL (PostgreSQL / MySQL / Google Spanner)**:
  - **優點**：強一致性 (ACID 屬性)、支援複雜的 JOIN 查詢。
  - **缺點**：垂直擴展 (Scale-Up) 昂貴，水平擴展 (Scale-Out) 非常複雜 (需實作 Sharding)。
- **NoSQL (MongoDB / Cassandra / Google Bigtable)**:
  - **優點**：Scheme-less (極度彈性)、原生支持水平擴展 (Scale-Out)、寫入效能極高。
  - **缺點**：多半只能達到最終一致性 (Eventual Consistency)、不支援複雜查詢。
  
### 📌 CAP Theorem & PACELC
- 系統無法同時滿足 Consistency (一致性)、Availability (可用性) 與 Partition Tolerance (分區容錯)。
- L4 面試必須解釋：「在這個設計中，遇到網路斷線時，我選擇犧牲 C 來保全 A (例如社群貼文)，或是犧牲 A 來保全 C (例如銀行轉帳)」。

### 📌 Sharding (分片) 與 Replication (抄寫)
- **Sharding**：將數據按照某個 Shard Key 分散到不同機器 (解決容量問題)。
  - **挑戰**：Global 二次排序 (Scatter-Gather)、跨 Shard 的 Transaction、Resharding 困難。
- **Replication**：同樣的數據複製多份到不同的 Node (解決高可用與讀取壓力)。
  - **挑戰**：Replication Lag (抄寫延遲) 導致的 Stale Read (讀到舊資料)。
