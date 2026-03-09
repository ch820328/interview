# Story: BIOS 環境變數 Bug（三方會議打破 Sunk Cost 僵局）

**適用題型 (Applicable Types):**
`✅ Type 1 衝突` `✅ Type 3 領導力` `✅ Type 6 Googleyness`

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **問題** | BIOS Garbage Collection Bug：環境變數超過上限後前面的變數遺失，直接 Block 產線 |
| **資深同事方案** | 取得 BIOS 剩餘上限空間，寫入 90% Size 測試是否遺失 |
| **我的反對** | 90% 壓測不符合真實 Scenario，可能引發 False Alarm，拖累產線良率 |
| **我的方案** | 以實際產線使用的變數數量為基準，乘安全係數，只需保證能存 200 個變數即 Pass |
| **對方阻力** | 資深同事已實作完畢（Sunk Cost），不願修改 |
| **化解手段** | 主動召集跨部門會議：主管 + BIOS RD + QA + 產線人員 |
| **關鍵轉折** | 讓產線人員親自說明實際使用數量，用「真實數據」取代「工程師意見」打破僵局 |
| **結果** | 採用我的方案，保證 200 個變數空間即 Pass，避免 False Alarm 並解除產線阻塞 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 1 — 衝突
> *"A senior engineer had already implemented the solution — and I fundamentally disagreed with it. The hardest part wasn't the technical argument. It was how to say that without making it personal, when the person had just sunk hours into writing the code."*

**強調重點：**
- Sunk Cost 心理 → 私下直接反對無效 → 召集跨部門會議
- 把焦點從「誰的 code 對」轉移到「Business Goal 是什麼」
- 產線人員的實際數據成為打破僵局的關鍵

---

### Type 3 — 領導力
> *"I saw the engineering team debating a solution that would hurt production yield — not because they were careless, but because nobody had brought the actual production data into the room. I decided to change that."*

**強調重點：**
- 主動識別「資訊不對稱」（工程師不知道產線實際使用量）
- 自己召集並主持跨部門會議（無職銜授權）
- 將「終端使用者視角」帶入技術決策

---

### Type 6 — Googleyness（做對的事 vs. 避免衝突）
> *"It would have been easier to let the senior engineer's solution go through — he'd already written it, and pushing back would create friction. I chose not to, because the solution would have hurt production yield."*

**強調重點：**
- 明知得罪人也要做對的事
- 沒有背後說壞話，而是正式召集會議公開討論
- 以終端使用者（產線）的利益為優先，而非工程師自尊

---

## 📖 完整 STAR

### Situation（情境）
產線測試工具遇到嚴重的 BIOS Bug：當環境變數超過上限，Garbage Collection 異常導致前面的變數遺失，直接造成產線測試失敗（Block 產線）。我們需要開發一個自動化檢測工具來防範此問題再發。

### Task（任務）
一位資深同事已實作完畢一套方案（取上限 90% 空間測試），並拿到 Code Review。我認為這個方案不符合真實 Scenario，且會引發 False Alarm 拖累良率，決定提出強烈反對意見。

### Action（行動）
**1. 識別阻力根源：** 資深同事有 Sunk Cost（已寫完），私下反對很難突破。我選擇不直接衝突，而是主動發起跨部門 Sync-up Meeting。

**2. 召集跨部門會議：** 邀請主管、BIOS RD 負責人、QA、以及**產線人員**（關鍵：把終端使用者拉進來）。

**3. 會議策略：**
   - 先釐清 Bug 最初的 Root Cause（建立共同認知基礎）
   - 讓**產線人員親自說明**他們實際使用的環境變數數量（讓數據自己說話）
   - 把焦點從「誰的 code 好」轉移到「我們真正要解決的 Business Goal 是什麼」

### Result（結果）
各方基於實際數據達成共識：極限測試（90%）不符合產線需求。最終採用我的方案：保證 BIOS 能儲存 200 個環境變數即 Pass。
- ✅ 解決 BIOS Bug 引發的產線阻塞
- ✅ 避免未來因過度測試造成的 False Alarm
- ✅ 讓終端使用者視角介入技術決策，打破工程師盲點

**Learning:** 在工程師分歧陷入僵局時，把「終端使用者的真實數據」帶進會議，往往比任何技術論點都更有說服力。

---

## ⚠️ 關鍵扣分提醒

| 常見錯誤 | 正確做法 |
|---|---|
| 沒說對方有 Sunk Cost | 明確說「他已經實作完了，所以這個反對更困難」|
| 沒說產線人員在會議中的關鍵作用 | 強調「讓終端使用者自己say出數字」才是打破僵局的武器 |
| 結果只說「採用我的方案」 | 說「避免了 False Alarm」才是業務層次的成果 |
