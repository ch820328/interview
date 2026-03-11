# Story: BIOS 安全性更新自動化通知系統 (從模糊需求到跨國架構落地)

**適用題型 (Applicable Types):**
`✅ Type 2 模糊性` `✅ Type 1 衝突與對齊` `✅ Type 3 影響力(無權威)` `✅ Type 5 優先級`

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **專案背景** | PM 要求在 BIOS 有重大安全性更新時，能及時通知負責 OEM 專案的 PM/Sales 聯絡客戶。 |
| **模糊性與痛點** | 過去 PM 需每天手動花 15~30 分鐘：下載 BIOS、解壓縮看修改紀錄、並對照自己私下維護的 Excel 表格才知聯絡誰。 |
| **跨部門依賴** | 需要整合**美國團隊 BIOS 發布資料**與**內部 IT 銷售資料**，但當下無適合的 API。 |
| **向上管理 (衝突)** | PM 不解為何需 4~6 週 ETA。我拆解技術流程（2-3 週等 API、0.5 週資料對接、0.5 週前端、0.5 週後端/DB），並請他動用業務影響力 Push API 產出以加速。 |
| **化解手段 (影響力)** | 說服 IT 開發 API：不談技術，而是強調商業價值「主動及時通知客戶，更有機會獲得後續訂單業務」。 |
| **我的方案結構** | 後端：2 個 Cron job 定時自動同步跨國/跨部門資料；前端：產出 PM 專屬 Search UI，一鍵產生 Mail 格式與精準 CC List。 |
| **量化成果** | PM 每天 15~30 分鐘的手動爬梳完全歸零，BIOS 更新一發布即無縫精準推播草稿。 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 2 — 模糊性 (Handling Ambiguity)
> *"I was handed a simple-sounding request: 'Notify PMs when there's a BIOS security update.' But beneath that request was a broken process where PMs spent 30 minutes every day manually downloading BIOS files just to check release notes. To automate this, I had to architect a data pipeline across three different departments."*
>
> **強調重點：**
> - 洞察模糊需求背後的真正痛點（PM 手工下載/解壓縮/比對 Excel）。
> - 跨平台資料碎片化：需整合內部 IT 與美國的系統資料。
> - 從「寄信工具」到「跨國自動化資訊流」的架構升級。

---

### Type 1 — 衝突處理與共識對齊 (Conflict & Alignment)
> *"My PM was extremely frustrated when I gave a 4 to 6-week ETA for what seemed like a 'simple email notification.' Instead of arguing, I mapped out the exact engineering breakdown and turned him into an ally to speed up the process."*
>
> **強調重點：**
> - PM 覺得只是「寄個信」，不理解為什麼要 4~6 週。
> - 拆解 ETA（API 等待 2-3 週、我方實作 1.5 週）。
> - 向上管理策略：給他槓桿，告訴 PM「如果你能動用業務影響力去 push 對方 API，我們時間能砍半」。

---

### Type 3 — 領導力與影響力 (Leadership & Influence)
> *"I needed an API that didn't exist, from an IT team that had their own priorities. To get their resources, I stopped talking about technical requirements and started talking about the business: proactive customer communication leads directly to new orders."*
>
> **強調重點：**
> - 說服平行團隊（IT）做他們原本不想做的事。
> - 轉換語言：不談「我們需要這個資料」，談「這對公司整體業務訂單的幫助」。
> - 串聯 PM、IT 與美國團隊，引領整個跨部門專案落地。

---

## 📖 完整 STAR (以 Type 2 模糊性為主軸)

### Situation（情境）
為了發送 BIOS 重大安全性更新通知，PM 過去每天必須花費 15~30 分鐘執行一套極度原始的流程：手動下載 BIOS 檔、解壓縮閱讀 release notes 看有無更新，然後再對照自己私下維護的 Excel 表格，查出該聯絡哪些 OEM PM/Sales。PM 希望能將這個流程自動化，但需求極度模糊，且缺乏現成資料源。

### Task（任務）
我的任務是將這個模糊的痛點，轉化為自動化的架構並實作推行。

### Action（行動）
**1. 釐清模糊性並推動跨部門合作：**
我盤點發現，要做到完全自動化，必須整合「美國團隊的 BIOS 發布系統」與「內部 IT 負責的 OEM 銷售名單」。當時 IT 並沒有合適的 API 能夠串接。為了說服忙碌的 IT 排入資源，我沒有提「PM 覺得很麻煩」，而是向 IT 主管強調商業價值：「如果系統能即時且主動地通知客戶資安更新，我們就更有機會獲得後續訂單業務」。IT 聽懂了商業價值，同意配合設計 API。

**2. 向上管理與期望值對齊 (Conflict Resolution)：**
我向 PM 提報了 4~6 週的 ETA。PM 初期難以理解「為什麼寄個信要這麼久」。我沒有爭論，而是拿出了硬核的工程拆解：
- 等待 IT 與美國 API 規格釐清到上線（2~3 週）
- 內部資料對接（0.5 週）
- 內部前端與後端/資料庫開發（各 0.5 週）
我不僅讓他看見全貌，更給了他解決方案：「核心瓶頸在於那 2-3 週的跨部門 API 開發，如果您能用業務端的影響力去 Push 對方，我們的 ETA 有機會立刻砍半。」這成功把 PM 的抱怨轉化為推進專案的盟友戰力。

**3. 系統實作與產品化設計：**
我設計了兩組 Cron Job，定時在背景將這兩地的異質資料同步入庫。在前端，我刻意不採用無腦的「全自動寄信」，而是設計了專屬搜尋 UI：系統會自動配對正確的客戶與業務，一鍵自動產出 **標準 Email 內容與龐大的 CC/BCC List草稿**。讓 PM 仍保有發信前的最終審核權 (Quality & Security Check)，同時省去所有拼湊資料的苦工。

### Result（結果）
- ✅ 成功說服 IT 建置跨國串接 API，在預期時程內完成專案上線。
- ✅ PM 每天 15~30 分鐘無效率的「人工肉眼檢查 BIOS / 比對 Excel」徹底歸零。
- ✅ 實現零時差精準推播草稿，大幅消除因人工疏漏而未通知客戶的潛在資安風險。

**Learning:** 面對模糊的跨國需求，工程師不能只當「接單的寫扣機器」。主動釐清依賴關係、用對方聽得懂的語言溝通 ETA，才是影響專案成敗的關鍵。

---

## ⚠️ 關鍵扣分提醒 (Critical Pitfalls)

| 常見錯誤 (Common Bugs) | 正確做法 (Fix) |
|---|---|
| 只說「我寫了兩個 Cron Job」 | 強調最困難的是「前期沒有 API，我主動跨部門協調爭取資源」，寫 Code 反而是最簡單的部分。 |
| 沒有解釋為什麼不用「全自動化」寄出 | 半自動 (生成 template 與 cc list) 往往是深思熟慮的結果，說明因為有商業/資安敏感性，需保留人類最後審核權（Engineering judgment）。 |
| PM 抱怨 ETA 太久時硬抗 | 正確展現 L4 影響力的方法是：「向 PM 揭露 Engineering Breakdown（拆解 4-6 週怎麼來的）並請求他動用業務端影響力協助催促 API進度」。 |
