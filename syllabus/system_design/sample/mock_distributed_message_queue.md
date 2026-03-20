# Distributed Message Queue (分散式訊息隊列)

## Requirements & Scale (需求與規模)

**Functional Requirements (功能需求):**
- Pub/Sub model with consumer groups. (支持消費者群組的發佈/訂閱模型。)
- Message persistence with 7-day retention. (訊息持久化儲存，保留期 7 天。)
- Partition-level ordering guarantees. (分區層級的順序保證。)

**Non-Functional Requirements (非功能需求):**
- High Availability for producers. (生產者端的高可用性。)
- High Durability (No data loss on broker failure). (高持久性，Broker 故障時不丟失數據。)
- Scalability to handle massive throughput. (可擴展以處理海量吞吐量。)

**Scale Numbers (規模數據):**
- **Throughput (吞吐量):** 1 million messages/sec (1M 訊息/秒).
- **Message Size (訊息大小):** 1 KB average.
- **Daily Volume (每日量):** ~86.4 TB.
- **Total Storage (總儲存):** ~1.8 PB (7 days, RF=3).

---

## Clarification Q&A (問答紀錄)

| Question (問題) | Answer (回答) |
|---|---|
| Global vs Partition Ordering? (全局還是分區順序？) | Partition-level is sufficient; global is a bottleneck. (分區層級即可；全域順序會成為瓶頸。) |
| Availability vs Consistency (CAP)? (可用性還是強一致性？) | Prioritize Availability for producers (AP). (優先保證生產者的可用性。) |
| Data Persistence Period? (資料保留多久？) | 7 days even after consumption. (即使已消費，仍保留 7 天。) |

---

## High-Level Architecture (高階架構圖)

```ascii
[Producers] --- (gRPC / Batching) ---> [ Load Balancer ]
                                            |
                                    [ Metadata Service ] <--- (KRaft / Raft)
                                            |
        -------------------------------------------------------------
        |                           |                               |
  [ Broker 1 ]                [ Broker 2 ]                    [ Broker 3 ]
  (Leader P0)                 (Leader P1)                     (Follower P0)
  [ Segmented Log ]           [ Segmented Log ]               [ Segmented Log ]
        |                           |                               |
        -------------------------------------------------------------
                                            |
                                    [ Consumer Groups ]
                                     (Pull / Zero-copy)
```

---

## Request Flows (請求流程)

**Write Flow (寫入流程):**
1. Producer fetches metadata to find the **Leader Broker** for a partition. (生產者獲取元數據，尋找分區的 Leader Broker。)
2. Producer batches messages and sends them via **gRPC**. (生產者將訊息打包成批，透過 gRPC 發送。)
3. Leader Broker writes to **Page Cache** (Sequential I/O). (Leader Broker 寫入 Page Cache，順序 I/O。)
4. Replication starts to Follower nodes. (開始同步資料至 Follower 節點。)

**Read Flow (讀取流程):**
1. Consumer pulls messages from the Leader via **Offset**. (消費者根據 Offset 從 Leader 拉取訊息。)
2. Broker uses **Zero-copy (sendfile)** to transfer data from Disk Cache to NIC. (Broker 使用零拷貝技術將資料從磁碟快取直接傳至網卡。)
3. Consumer updates Offset after successful processing. (處理成功後，消費者更新 Offset。)

---

## Trade-off Table (權衡分析表)

| Decision (決策) | ✅ Gain (亮點) | ❌ Sacrifice (代價) |
|---|---|---|
| **Append-only Log** | High Sequential Write Speed. (極高的順序寫入速度。) | Cannot update/delete specific messages. (無法更新或刪除特定訊息。) |
| **Pull Model** | Consumer-side Back-pressure handling. (消費者端的背壓處理。) | Slight increase in end-to-end latency. (端到端延遲略微增加。) |
| **Random Salt on Hot Keys** | Solves Hot Partition bottleneck. (解決熱點分區瓶頸。) | Loses ordering for salted keys. (失去加鹽 Key 的順序性。) |

---

## Final Evaluation (最終評估)

1. **Overall Rating (整體評分):** **Strong Hire**
2. **Requirements & Scoping (需求定義):** Excellent. Properly identified the need for high ingest availability and the specific constraints of partition-level ordering. (優異。正確識別高攝入可用性的需求以及分區順序的限制。)
3. **Architecture Depth (架構深度):** L5 Standard. Deep understanding of Zero-copy, Page Cache pollution, and memory management using `fadvise`. (達到 L5 標準。深入了解零拷貝、Page Cache 污染以及使用 `fadvise` 的內存管理。)
4. **Resilience & Bottlenecks (彈性與瓶頸):** Proactively proposed **Adaptive Salting** for hot partitions and **Tiered Storage** for workload isolation. (主動提出對熱點分區的自適應加鹽以及用於負載隔離的分層儲存。)
5. **Actionable Corrections (行動建議):** The candidate is clearly operating at or above the L4 bar. Recommend focusing on niche failure modes in KRaft/metadata layers for L5 prep. (候選人顯然已達到或超過 L4 標準。建議專注於 L5 準備中 KRaft/元數據層的細微故障模式。)

---

## Technical Term Dictionary (技術術語表)

| Term (術語) | English Definition | Chinese Translation (中文翻譯) |
|---|---|---|
| **Zero-copy** | Technique to minimize data copying between buffers. | **零拷貝**：減少數據在緩衝區間搬運的技術。 |
| **Page Cache** | Transparent cache of disk data in kernel memory. | **頁快取**：內核內存中磁碟數據的透明快取。 |
| **Adaptive Salting** | Adding random bits to keys to spread traffic on hot partitions. | **自適應加鹽**：在 Key 中加入隨機位元以分散熱點分區流量。 |
| **KRaft** | Raft consensus integrated directly into the event log. | **KRaft**：直接集成在事件日誌中的 Raft 共識演算法。 |

Syllabus saved to: `/home/interview/syllabus/system_design/distributed_message_queue.md`
Syllabus 已儲存至：`/home/interview/syllabus/system_design/distributed_message_queue.md`
