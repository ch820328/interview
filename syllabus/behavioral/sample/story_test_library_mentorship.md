# Story: 測試腳本輔助套件與文件庫 (自動化測試 Onboarding 優化)

**適用題型 (Applicable Types):**
`✅ Type 6 Googleyness (Mentorship/幫助他人)` `✅ Type 3 影響力(無權威)` `✅ Type 2 模糊性`

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **專案背景** | 開發自動化測試時，需頻繁操作多種異質 API (樹莓派 GPIO、Windows 特定 Tool、OCR、第三方 Web API 等)。 |
| **新人痛點** | 過去 API 文件只寫參數且年久失修。新人必須自己去翻舊的 Git repo 程式碼，自己發 Request 看 Response 慢慢猜，導致極高的 Onboarding 挫折感。 |
| **我的主動行動 (Googleyness)** | 在開發中只要用到相關 API，就順手將其封裝成物件導向的 Class，並建立一份活的 API 文件，包含實際 Response 與範例。 |
| **無人指派的影響力** | 這並非主管指派的 KPI，而是出於「讓下一個開發者更輕鬆」的工程師文化 (Act like an Owner)。 |
| **量化成果** | 封裝了至少 5 個核心服務的 API Class；後續有 30+ 以上的自動化測試項目都直接依賴這些共用元件，徹底消滅了新人「看 Code 猜 API」的時間浪費。 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 6 — Googleyness (Mentorship & Team Capability)
> *"I noticed that every new hire was struggling with the exact same problem: our documentation was outdated, they had to dig through old Git commits just to guess what an API would return. So instead of just answering their questions one by one, I decided to fix the system for everyone who came next."*
>
> **強調重點：**
> - 深刻的同理心：觀察到新人「看 Code 猜 API」的痛苦。
> - 解決方案：從「一對一回答問題」升級到「建立系統化的 Class 與活文件」。
> - 展現「幫助他人成功」的核心價值。

---

### Type 3 — 領導力與影響力 (Leadership Without Authority)
> *"Nobody asked me to build a unified testing library or write the API documentation. But when I saw that our test development was blocked by a fragmented ecosystem of RasPi, Windows, and Web APIs, I took ownership of standardizing it alongside my regular tasks."*
>
> **強調重點：**
> - 無人授權／非 KPI 項目（Proactive Ownership）。
> - 利用日常開發的「順手」來逐步推動架構標準化。
> - 建立團隊的 Coding Standard，影響了整個部門的開發習慣。

---

## 📖 完整 STAR (以 Type 6 Mentorship 為主軸)

### Situation（情境）
我們的自動化測試環境涵蓋了各種異質系統：控制硬體的樹莓派 (GPIO)、專屬 Windows 的執行工具、純軟體的 OCR 辨識，以及操作第三方應用的 Web API。我發現新人加入時面臨巨大的障礙：現存的 API 文件年久失修，甚至只寫了參數。新人如果不知道怎麼用，只能自己去翻舊的 Git repo 程式碼，自己實際去發 Request 測 API Response，看 Code 慢慢猜，這導致 Onboarding 曲線極長且充滿挫折。

### Task（任務）
我的主要任務依然是開發分配給我的自動化測試項目。但我意識到，如果不解決這個基礎建設問題，整個團隊的擴展能力會被嚴重拖累，每個新人都必須重新踩一次同樣的坑。

### Action（行動）
**1. 化被動為主動的物件導向封裝 (Incremental Standardization)：**
我採取「童子軍守則」。每次我在開發新測項、只要碰到某個服務的 API，我不會只把扣寫在自己的 Script 裡。我會刻意將它抽離，封裝成一個通用、具備標準介面的 Class 物件。

**2. 建立活的 API 文件庫 (Documentation as Code)：**
除了封裝 Class，我同時強制建立對應的 API 文件。因為我知道舊文件爛在哪裡，所以我特別在文件裡補上「實際的 Response 結構」與「Example Usage」。這讓文件不再只是生硬的規格，而是拿來就能跑的範本。

**3. 推廣與指引 (Mentorship in Action)：**
在 Code Review 或新人剛進來時，我不只是找出他們的 Bug，我會直接指引他們看我建立的文件，並告訴他們：「下次需要控制 Web API 或 OCR，可以直接呼叫這個 Class 的 Method。」

### Result（結果）
- ✅ 徹底改變了團隊的 Onboarding 體驗。新人不再需要浪費時間「看舊 Git Code 猜 API」，而是可以直接引用封裝好的 Class 與看實際範例。
- ✅ 團隊的測試代碼品質與可維護性統一提升，我成功將至少 5 個核心服務的 API 封裝成了標準 Class。
- ✅ 這套共用元件與文件庫，後續至少支撐了 30+ 個以上的自動化測試項目的開發，即使這最初根本不是我的 KPI。

**Learning:** 最好的 Mentorship 不只是口頭教導或丟文件，而是去優化整個系統環境，消除開發過程中的「猜測工時」，讓做對的事情變得跟呼吸一樣簡單。

---

## ⚠️ 關鍵扣分提醒 (Critical Pitfalls)

| 常見錯誤 (Common Bugs) | 正確做法 (Fix) |
|---|---|
| 把焦點全放在技術多難 | 樹莓派或 OCR 的實作細節不重要。重點是你解決了「看舊 code 猜 API Response」這個非常強的人性痛點。 |
| 聽起來像是你一個人的專案 | 必須強調這對「團隊」的幫助 (30+ 測試引用)，以及你如何帶動新人使用這套 Class（展現 Leadership）。 |
| 缺乏量化數據 | 面試時一定要念出：5個封裝的服務、30+的測試腳本引用，這能立刻證明你的影響半徑 (Blast Radius)。 |
