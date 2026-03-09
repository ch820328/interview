# Story: BSP Flash 流程優化（產線刷機架構改革）

**適用題型 (Applicable Types):**
`✅ Type 1 衝突` `✅ Type 3 領導力` `✅ Type 5 優先級`

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **背景** | Jetson Orin 產線刷機需在機器上重新 Compile，每台耗時 15 分鐘，且環境不一致有潛在品質風險 |
| **PM / 產線立場** | SOP 已在運作，不願承擔改變流程的未知風險 |
| **我的方案** | 在 Build Server 上預先 Compile Image Blob，再直接 Release 給產線刷入 |
| **數據說服 PoC** | 親自做 PoC，邀產線主管觀看：新架構支援多台平行刷機，消滅環境不一致 |
| **資安論據** | 引用公司歷史教訓（BIOS 測試版外流事件），將「收回 Compile 權限」定位為資安防禦機制 |
| **結果** | 生產工時從 15 分鐘縮減至 8 分鐘以內（↓50%+），版控與環境建置錯誤歸零 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 1 — 衝突
> *"PM and the production line both rejected my proposal immediately. I had to find a different lever — and I found it in a past security incident that everyone had already forgotten."*

**強調重點：**
- 初次拒絕的原因（不想承擔變更風險）
- 兩個說服武器：PoC 效率數據 + 資安歷史教訓
- 把技術爭論提升到「公司級品質保證」層次

---

### Type 3 — 領導力
> *"I proactively redesigned a production workflow that nobody asked me to redesign — because I saw it was wasting 50% of our deployment time and creating invisible quality risks."*

**強調重點：**
- 主動發現問題並定義解法（無人指派）
- 研究 NVIDIA 官方量產白皮書後提出架構方案
- 帶領跨部門（PM + 產線）接受改革

---

### Type 5 — 優先級
> *"I had to choose: keep a process that 'works' but wastes 15 minutes per device — or invest 2 weeks in a redesign that permanently removes the bottleneck. I chose to make the case for the redesign."*

**強調重點：**
- 短期穩定性 vs. 長期效率的 Trade-off 決策
- 15 分鐘 → 8 分鐘，50% 工時降低的業務價值
- 用 ROI 邏輯說服保守的 PM 和產線

---

## 📖 完整 STAR

### Situation（情境）
Jetson Orin 產線的刷機流程需要在每台機器上重新 Compile Image，這導致：
1. 每台機器部署時間長達 15 分鐘
2. 每次編譯環境可能不一致（環境變數、工具版本差異）
3. 無法平行化，產能擴充受限

### Task（任務）
我研究了 NVIDIA 官方量產白皮書後，決定推動架構改革：在 Build Server 上預先 Compile Image Blob，再直接 Release 給產線。但 PM 和產線主管均表示現有 SOP 已在運作，不想冒變更風險。我需要說服他們。

### Action（行動）
**1. PoC + 邀請觀看（數據說服）：**
親自完成 PoC，邀請產線主管現場觀看：新架構支援多台機器平行刷機，能大幅擴充產能並消除環境不一致的隱患。讓他們親眼看到效果而非只聽簡報。

**2. 資安論據（利用對方的痛點）：**
為了消除 PM 對「改變流程」的疑慮，我主動引用公司過去的慘痛教訓——BIOS 開發時曾發生測試版外流的資安事件。我向 PM 強調：將 Compile 權限收回內部 Build Server，是防止出廠品質事故與機密外洩的「最佳資安防禦機制」。這成功將技術性爭論提升為公司級品質保證議題。

### Result（結果）
PM 和產線主管均被數據與風險評估說服，順利導入並標準化新流程。

| 指標 | 前 | 後 |
|---|---|---|
| 每台刷機時間 | 15 分鐘 | < 8 分鐘（↓50%+）|
| 環境建置錯誤 | 持續存在 | 歸零 |
| 版控錯誤 | 持續存在 | 歸零 |
| 平行化能力 | 無（逐台）| 多台平行 ✅ |

**Learning:** 面對跨部門的流程改革阻力，「技術比較好」一句話沒有用；必須用「實測數據」加上「對方的痛點（過去的資安風險）」，才能從更高格局推動組織變革。

---

## ⚠️ 關鍵扣分提醒

| 常見錯誤 | 正確做法 |
|---|---|
| 只說「我改了流程，效率提升了」 | 必須說出初期遭到拒絕，以及你如何克服阻力 |
| 忘記說資安論據 | 資安論據是這個故事最獨特的說服武器，一定要說 |
| 沒說 PoC 是親自做的 | 強調「我親自做 PoC，並邀請產線主管觀看」—— 這是 Ownership 信號 |
