# Technical Core: 分散式數據一致性 — LWW vs. CRDTs 深度大師課

> **導讀**：在離線優先 (Offline-first) 的移動端或分散式系統中，數據一致性 (Data Consistency) 是最難跨越的技術鴻溝。本文從 CAP/PACELC 定理出發，深度剖析 Last Write Wins (LWW) 與 Conflict-free Replicated Data Types (CRDTs) 的底層機制與選型權衡。

---

## 🏗️ 第一章：分佈式理論基石 (Theoretical Foundation)

### 1. CAP 定理與 PACELC 擴展
在分佈式系統中，我們熟知 CAP（Consistency, Availability, Partition Tolerance）。但在實務中，**PACELC** 定理提供更完整的視角：
- **P (Partition)**：如果發生分區，必須在 **A (Availability)** 與 **C (Consistency)** 間取捨。
- **E (Else)**：在沒有分區的正常狀態下，必須在 **L (Latency)** 與 **C (Consistency)** 間取捨。

> [!NOTE]
> **Offline-first 的選擇**：由於離線狀態本質上是長期的網路分區 (P)，我們必須優先保證 **可用性能 (A)** 與 **低延遲 (L)**，這意味著我們必須接受 **最終一致性 (Eventual Consistency)**。

---

## 🧬 第二章：時間與因果關係 (Time & Causality)

在分散式系統中，「時間」是不可信的。

### 1. 牆上時鐘 (Wall-clock Time) 的陷阱
由於 **時鐘偏移 (Clock Drift)**，設備 A 的 12:00 可能在設備 B 實際是 11:59。如果單純依賴系統時間進行 LWW，會導致因果關係顛倒。

### 2. 邏輯時鐘與向量時鐘 (Vector Clocks)
為了維護因果關係，我們引入了邏輯時鐘：
- **Lamport Clock**：單純的計數器，用於確定事件的偏序關係。
- **Vector Clock**：每個節點維護一個數組 `[V1, V2, ... Vn]`。這能幫助系統判斷兩個變更是「先後發生」還是「同時發生 (Concurrent)」。當兩組向量時鐘呈「不可比」狀態時，即發生衝突。

#### 向量時鐘更新範例：
| 事件 | 節點 A | 節點 B | 狀態 [A, B] |
| :--- | :--- | :--- | :--- |
| A 修改 | `A++` | - | `[1, 0]` |
| A 傳給 B | - | `recv(A)` | `[1, 0]` |
| B 修改 | - | `B++` | `[1, 1]` |
| A, B 同步 | `merge` | `merge` | `[1, 1]` |

### 3. 因果一致性 (Causal Consistency)
比起單純的最終一致性，因果一致性確保如果 A 發生在 B 之前，那麼所有節點都必須在看到 B 之前先看到 A。這在「討論區回覆」或「交易生命週期」中至關重要。

---

## 🧬 第三章：Last Write Wins (LWW) — 務實的一致性

這是 **Baby Tracker** 採用的機制，其核心是「以權威時鐘為準」。

### 運作演算法
1. 每個更新封包帶有 `timestamp` 與 `device_id`。
2. 伺服器接收到多個更新時：
   - 比較 `timestamp`，大者勝出。
   - 若 `timestamp` 相同，比較 `device_id` (確定性衝突解決)。

### 實務演算法：Healing 機制
當 Client 推送舊資料時，Server 會回傳一個特殊的 **Heal Packet**。這確保了 Client 能迅速從分歧狀態收斂回 Source of Truth。

#### Healing 偽代碼實作：
```typescript
function handlePush(clientData, serverState) {
    if (clientData.version < serverState.version) {
        // 客戶端版本過舊，觸發 Healing
        return {
            status: "HEAL",
            correctState: serverState.data,
            newVersion: serverState.version
        };
    } else {
        // 執行 LWW 合併
        const newState = mergeLWW(clientData, serverState);
        return { status: "OK", version: newState.version + 1 };
    }
}
```

---

## 💎 第四章：CRDTs — 數學保障的無損合併

CRDTs 是一類特殊的數據結構，確保資料可以從多個路徑併發修改並自動合併。

### 1. 兩大分類
- **State-based (CvRDT)**：傳輸整個資料狀態，透過 **Join (LUB)** 操作進行合併。
- **Operation-based (CmRDT)**：傳輸「操作指令 (Ops)」，要求網路保證「不丟包、不重複且按順序遞交」。

### 2. 數學定義：半格 (Semilattice)
State-based CRDTs 的核心是 **Join (LUB - Least Upper Bound)** 操作。一個資料結構必須滿足：
- **Idempotent (自等性)**: `x ⊔ x = x`
- **Commutative (交換性)**: `x ⊔ y = y ⊔ x`
- **Associative (結合性)**: `(x ⊔ y) ⊔ z = x ⊔ (y ⊔ z)`
只有滿足這三個特性的資料結構，才能保證在任何同步順序下，最終狀態完全收斂。

### 3. 常見 CRDT 模型
| 模型 | 全稱 | 運作邏輯 |
| :--- | :--- | :--- |
| **G-Counter** | Grow-only Counter | 只能增加，對數組取 Max 即可合併。 |
| **PN-Counter** | Positive-Negative Counter | 由兩個 G-Counter 組成（正向與負向）。 |
| **OR-Set** | Observed-Remove Set | 為每個元素標註唯一的 Tag，解決「同時新增與刪除」的爭議。 |
| **LWW-Element-Set** | LWW 元素集合 | 每個元素帶時間戳記，刪除紀錄 (Tombstone) 也帶時間戳記，取大者。 |

---

## ⚖️ 第五章：深度選型矩陣 (The Selection Matrix)

| 維度 | **LWW (Last Write Wins)** | **CRDTs (Automerge/Yjs)** |
| :--- | :--- | :--- |
| **合併精確度** | 粗糙，會丟失「非贏家」修改 | **精確，支援 Character-level 合併** |
| **儲存與傳輸** | **極低 (僅當前狀態)** | **高 (需儲存所有點位/步進元數據)** |
| **CPU 開銷** | 低 | 高 (需在本地計算所有 Ops 的收斂) |
| **離線衝突感官** | 可能發生「覆蓋」感 | **完全無感透明** |
| **代表案例** | Cassandra, DynamoDB, Baby Tracker | Figma, Notion, Google Docs |

---

## 🛠️ 第六章：進階實作模式 (Advanced Patterns)

### 1. 混合一致性模型 (Hybrid Models)
在真實的大型系統中，單一模型往往不夠：
- **LWW 用於純量 (Scalars)**：如用戶的「暱稱」、「性別」，這類資料衝突代價小。
- **CRDT 用於陣列與文本 (Sequences)**：如「聊天訊息列表」或「協作編輯內容」。
- **強一致性用於金流 (Transactions)**：使用 Paxos/Raft 協議處理帳戶餘額。

### 2. 衝突偵測 (Conflict Detection)
即使是 LWW，我們也需要精確偵測衝突。
- **Version Vectors**：在 API Header 中攜帶，伺服器比對後決定是 `Apply` 還是 `Conflict (409)`。

---

## 🏢 第七章：工業界實作案例

### 1. Amazon DynamoDB (LWW)
DynamoDB 在預設情況下使用 LWW 進行物理層級的衝突處理，這為了追求極致的吞吐量與低延遲。

### 2. Figma (Op-based CRDT 變種)
Figma 為了實現多人即時協作，使用了基於操作的 CRDT，確保每個人的圖層縮放與移動都能精確合併。

---

## 📈 第七章：面試兵法 (Resume Highlights)

### 如何描述同步架構經驗？
- **深度剖析**：不要只說「我用了 LWW」，要說「我分析了我們資料的 **Write/Read Ratio** 與 **Conflict Probability**，認為 LWW 配合 **Healing 機制**在行動端資源受限下是更優的權衡」。
- **理論連結**：將實作連結到 **PACELC 定理**，展現你對 Latency 與 Consistency 之間取捨的深刻理解。

---

### 關鍵金句總結
- **「分散式系統中沒有時間，只有因果。LWW 是對物理時間的妥協，而 CRDTs 是對數學邏輯的堅持。」**
- **「在資料模型相對簡單的場景下，LWW 配合有效的補償機制 (Healing)，往往能換取比 CRDTs 更佳的性能與使用者體驗。」**
- **「架構設計的精髓不在於選擇最強大的技術，而在於選擇最能符合當前業務邊界與資源限制的方案。」**

---

## 📡 第九章：實時通訊與廣播 (Real-time Sync)

離線同步通常配合實時通訊來減少衝突窗口：

1. **WebSockets / Socket.io**：當伺服器端收到 `push` 請求後，除了更新資料庫，還會立即向該用戶的所有在線設備發送一個 `INVALIDATE` 信號，提示設備立即進行一次 `pull` 同步。
2. **Pub/Sub (Redis)**：在多節點後端架構中，利用 **Redis** 作為消息中間件來達成同步事件的跨伺服器傳遞。
3. **Delta Sync (增量傳輸)**：相比於傳統的「全量傳回」，增量傳輸僅傳輸變動的欄位 (Diffs)，這能避免在大數據量下造成的網路塞車。

---

## 🌳 第十章：反熵機制 (Anti-Entropy) — Merkle Trees

當系統長期離線或遭受損壞，導致資料庫不一致但又不知道具體是哪一筆錯時，會使用 **Merkle Trees (哈希樹)**：
- **原理**：將資料分區（Buckets）建立哈希樹，兩點（Client vs Server）同步時，只需比對根哈希 (Root Hash)。若不一致，則逐層向下比對，直到找到分歧的資料區塊。
- **優勢**：極大化減少比對時需要的傳輸數據量。這是 **Cassandra**、**Riak** 與 **Git** 的核心底層技術。

---

## ⚖️ 第十一章：CRDTs vs. OT (Operational Transformation)

在共筆編輯領域，除了 CRDTs，另一個響亮的技術是 **OT**：
- **OT (Google Docs 採用的方案)**：依賴於一個「中央伺服器」來進行操作的座標轉換與定序。
- **CRDTs (Figma 採用的方案)**：去中心化。資料本身俱有合併邏輯，不需要中央權威。
- **結論**：對於 Baby Tracker 這種可能長期斷網且不具備中央強權威環境的 App，我們傾向於類 CRDT 的邏輯（即便我們使用了簡化版的 LWW）。

---

## 🔐 第十二章：分散式同步中的安全性 (Security)

在 Local-first 架構中，安全性不再只是伺服器端的驗證，而是需要跨層級考慮：

1. **本地存儲加密**：即便在離線狀態下，手機端資料庫也必須使用 SQLCipher 等技術加密。
2. **時鐘篡改防護**：防止客戶端惡意篡改本地時間來「贏得」LWW。
   - **對策**：伺服器端應使用 `received_at` 作為次要判斷權重，或是在同步時校準 (Clock Sync) 客戶端時間。
3. **因果關係驗證**：確保同步流中，父節點的變更絕對不會發生在子節點之後。

---

## 🏗️ 第十三章：開源生態與工具鏈 (Ecosystem)

當您決定在專案中導入這些概念時，可以考慮以下成熟工具：

### 1. Yjs & Automerge
- **適用場景**：前端實作 Rich-text、白板協作。
- **特性**：基於 Op-based CRDT 優化，具備極高的合併性能。

### 2. RxDB & WatermelonDB
- **適用場景**：本地資料存儲與同步。
- **特性**：提供離線緩存的第一方支持，並能與 LWW 或客製化同步邏輯整合。

### 3. Gun.js
- **適用場景**：去中心化 (P2P) 同步。
- **特性**：基於圖 (Graph) 的同步協議，天生支持分佈式。

---

## 🔐 第十章：分散式同步中的安全性 (Security)

在 Local-first 架構中，安全性不再只是伺服器端的驗證，而是需要跨層級考慮：

1. **認證與授權**：即便在離線狀態下，本地數據庫也必須加密，防止物理接觸導致的資料外洩。
2. **Sync ACLs (存取控制清單)**：伺服器在接收同步請求時，必須嚴格核對 `device_id` 與 `user_token`。
3. **資料正確性驗證**：防止客戶端惡意篡改 `timestamp` 來贏得 LWW 競爭。通常伺服器會加上 `server_received_at` 作為最終判斷依據。

---

## 💡 第十一章：面試兵法 (Interview Strategy)
