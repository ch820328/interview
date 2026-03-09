# Story: NVSSVT Portal 遷移（帶領 30+ 人從 CLI 到集中式平台）

**適用題型 (Applicable Types):**
`✅ Type 2 模糊性` `✅ Type 3 領導力` `✅ Type 5 優先級`

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **背景** | 30+ 位工程師各自使用客製化的本地 CLI 工具和設定檔，導致環境飄移（Configuration Drift）|
| **核心痛點** | 同一個測試在 A 電腦過、在 B 電腦失敗；無法追蹤誰的設定是正確的 |
| **我的解法** | 設計並建立集中式 Go/Vue Web Portal，作為「中央控制平面（Centralized Control Plane）」 |
| **架構精髓** | 把測試環境配置的 Source of Truth 從個別 RD 手中抽離，統一由 Admin 在 Portal 管理 |
| **技術選擇** | Go（後端）+ Vue.js（前端）|
| **成果** | 消滅環境飄移，團隊「自然而然」自願轉換，因為穩定性顯著優於舊工具 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 2 — 模糊性
> *"There was no spec, no clear owner, and no one telling me to fix it. I just saw 30+ engineers all carrying their own fragmented configurations — and realized someone had to solve this at the architecture level, not just patch it."*

**強調重點：**
- 沒有人指派，自己識別系統性問題
- 主動定義解法層次（架構層 vs. 工具層）
- 如何在無明確需求下設計出「中央控制平面」

---

### Type 3 — 領導力
> *"I led a 30-person team migration from fragmented CLI tools to a centralized portal — not by mandate, but by building something so reliable that adoption happened naturally."*

**強調重點：**
- 帶領 30+ 人轉換工具（Leading without authority）
- 不是強制，而是靠工具的穩定性讓人自願使用
- 架構決策：把問題從「工具難用」提升到「資訊治理」層次

---

### Type 5 — 優先級
> *"I had to decide: keep everyone productive in the short term with their existing tools, or invest in fixing the root cause — environment inconsistency that was silently corrupting test results for months."*

**強調重點：**
- 短期生產力 vs. 長期系統健康的 Trade-off
- 環境飄移是「潛在成本」，不易被直接看見 → 需要量化說服
- 架構投資的長期 ROI

---

## 📖 完整 STAR

### Situation（情境）
部門內 30+ 位工程師都在使用各自客製化的本地設定檔與 CLI 工具進行測試。這造成嚴重的 Configuration Drift：同一份測試腳本在不同工程師的電腦上可能得出不同結果，而沒有人知道哪份設定才是正確的。

### Task（任務）
作為資深工程師，我決定從架構層面解決這個問題，而不是繼續讓大家各自修補自己的環境。目標：建立一個讓整個部門收斂到同一套配置的機制，且不強迫改變——透過工具本身的優越性讓人主動遷移。

### Action（行動）
**1. 架構定義（中央控制平面）：**
設計 Web Portal 不只是一個 UI，而是將測試環境配置的 Source of Truth 從個別 RD 手中抽離，統一交由 Admin 在 Portal 管理。這從根本上消除了本地設定錯誤的可能性。

**2. 技術選型（Go + Vue）：**
選擇 Go 作為後端（高效能、型別安全、易於部署），Vue.js 作為前端（低學習成本，部門熟悉）。

**3. 遷移策略（靠穩定性驅動採用）：**
不發強制通知要求所有人切換，而是在新 Portal 上線後持續展示它的穩定性與一致性。當工程師反覆遇到舊工具的環境問題時，Portal 成為他們自然的替代選擇。

### Result（結果）
- ✅ 消滅 Configuration Drift，測試結果跨機器一致
- ✅ 30+ 位工程師自願遷移，無需強制推行
- ✅ 測試環境的 Source of Truth 被集中管理，大幅降低 onboarding 新人的成本

**Learning:** 真正的技術領導力不靠強制，而是建造一個讓人寧願使用、不想回頭的系統。

---

## ⚠️ 關鍵扣分提醒

| 常見錯誤 | 正確做法 |
|---|---|
| 說「我做了一個 Vue.js 前端」 | 說「我設計了一個中央控制平面，解決的是組織級的資訊治理問題」|
| 沒說 Configuration Drift 的具體危害 | 明確說「同一測試在 A/B 電腦結果不同，沒有人知道哪個是對的」|
| 沒說遷移策略 | 說明「靠穩定性驅動自願採用，而非強制」|
