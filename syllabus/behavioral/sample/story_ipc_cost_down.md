# Story: IPC 規格降級失敗（從現場物理改裝到系統性研發標準）

**適用題型 (Applicable Types):**
`✅ Type 4 失敗與反思 (Failure & Resilience)` `✅ Type 1 衝突與對齊` `✅ Type 3 領導力` `✅ Type 5 優先級` `✅ Type 7 技術權衡`

---

## 🔑 核心事實 (Core Facts)

| 項目 | 內容 |
|---|---|
| **專案背景** | 工控系統開發案，面臨極端成本控制壓力。 |
| **失敗點** | 接受主管將 IPC 規格從 4 埠降至 2 埠的決策，未提供足夠數據挑戰此風險。 |
| **危機發生** | 客戶要求增加新模組，硬體連接口與空間完全耗盡。 |
| **補救行動** | 現場評估散熱與結構後，親自進行物理改裝（切削），手動騰出空間。 |
| **量化後果** | 雖然滿足需求，但現場改裝成本（差旅、人工、風險）是預留成本的 50 倍。 |
| **系統性改變** | 建立「硬體選型檢查表」與「風險矩陣」，規定必須保留 20-30% 擴展餘裕。 |

---

## 🎯 切角開場白 (Pivot Openings)

### Type 4 — 失敗、反思與韌性 (Failure & Resilience)
> **English:** "The most significant failure in my career wasn't a bug in code, but a failure to design for the future. I accepted a cost-cutting decision for an industrial PC that left zero room for expansion, which eventually forced me to perform 'physical surgery' on hardware at a customer site. Here is how that failure transformed our entire hardware selection process."
>
> **中文：** 「我職業生涯中最重大的失敗不是程式碼漏洞，而是未能為未來而設計。我當時接受了一個降低成本、將工業電腦規格壓到極限的決定，這最終迫使我必須在客戶現場對硬體進行『物理手術』。這次失敗徹底改變了我們整個硬體選型流程。」

---

### Type 1 — 衝突處理與共識對齊 (Conflict & Alignment)
> **English:** "I once failed to influence my manager on a critical hardware decision because I used qualitative arguments instead of quantitative data. We chose a low-spec IPC to save 15% in costs, which later resulted in recovery costs 50 times higher than the savings."
>
> **中文：** 「我曾因使用定性描述而非定量數據，而未能成功影響主管的一項關鍵硬體決策。我們為了節省 15% 的成本而選用低規電腦，導致後來的修復成本高達節省金額的 50 倍。」

---

### Type 3 — 領導力與影響力 (Leadership & Influence)
> **English:** "I turned a major production crisis into a new company standard. After discovering our hardware selection process lacked expansion buffers, I led a cross-functional post-mortem that forced Procurement and PMs to adopt a new risk-based hardware checklist."
>
> **中文：** 「我將一場嚴重的生產危機轉化為新的公司標準。在發現硬體選型缺乏擴展緩衝後，我主動召集了跨部門檢討會，推動採購與 PM 團隊採用基於風險的硬體檢核清單。」

---

### Type 7 — 技術難題與權衡 (Technical Trade-offs)
> **English:** "I once compromised on hardware specs to meet an aggressive cost-down goal, which created massive technical debt. When the system hit its limit, I had to physically modify the hardware on-site. Here is how I handled the immediate fallout and changed our engineering culture to balance cost with technical safety margins."
>
> **中文：** 「我曾為了達成積極的降本目標而在硬體規格上妥協，這帶來了巨大的技術債。當系統達到極限時，我必須在現場進行物理改裝。這是我如何處理這場危機，並改變團隊文化，在成本與技術安全餘裕之間取得平衡的故事。」

---

## 📖 完整 STAR (Full Narrative)

### Situation (情境)
在大陸負責一項工控系統開發案時，主管為了極端化成本控制（Cost Down），要求將工業電腦（IPC）規格降級，從 4 個 USB 埠減為 2 個，且體積縮小，導致機構空間極度緊湊。

### Task (任務)
我是系統開發負責人，雖然當時察覺擴展性受限，但受限於績效壓力與缺乏數據，我接受了該決定。我的任務是確保軟體能在這台受限的 IPC 上運行。

### Action (行動)
**1. 補救與風險權衡 (Risk Trade-off):**
當客戶要求增加新模組時，系統已無空間。由於重新訂購高規硬體需 4 週，會造成客戶停機巨大損失，我決定在現場進行「物理改裝」。我親自動手切削非承重部位騰出空間，並在改裝後使用**熱感儀進行壓力測試**，確保散熱符合工業等級底線。

**2. 影響力反思 (Influence Reflection):**
事後我反思失敗原因：我當時只用了「改起來很麻煩」這種感性訴求。我意識到管理者看重的是「即時 KPI」，而我應該展示「延遲成本 (Cost of Delay)」與風險期望值。

**3. 系統化變革 (Systemic Change):**
我主動召集採購與 PM 召開**事後檢討會 (Post-mortem)**。我展示了維修費與人工費高達節約金額的 50 倍，以此推動將「20-30% 擴展冗餘」寫入研發流程 (NPI Process)。

### Result (結果)
- ✅ 成功在 48 小時內恢復系統運作，避免產線長期停機。
- ✅ 建立「硬體選型檢查表」，現在開發團隊選型時必須量化擴展性風險。
- ✅ 讓採購與 PM 簽署風險聲明，將「技術隱患」轉變為「業務決策」。

**Learning:** 為當下設計就是對未來的失敗。真正的影響力來自於用數據與業務損益來定義風險。

---

## ⚠️ 關鍵扣分提醒 (Critical Pitfalls)

| 常見錯誤 (Common Bugs) | 正確做法 (Fix) |
|---|---|
| 只說自己修好了硬體 | 必須強調「為什麼當初沒能阻止決策」的反思。 |
| 把責任推給主管愛省錢 | 承認自己缺乏數據化溝通的能力 (Qualitative vs. Quantitative)。 |
| 沒提到散熱與結構驗證 | 物理改裝很危險，必須提到「數據底線」（如熱感儀測試）來展現工程嚴謹性。 |

---

## 📘 技術名詞字典 (Technical Term Dictionary)

| Term (術語) | English Definition | 中文解釋 |
|---|---|---|
| IPC | Industrial PC used for automation | 工業電腦 |
| Expansion Overhead | Reserved ports or space for future use | 擴展冗餘 / 緩衝空間 |
| Cost of Delay | The economic impact of delaying a project or feature | 延遲成本 |
| NPI Process | New Product Introduction process | 新產品導入流程 |
| Post-mortem | Analysis of a project after failure to learn lessons | 事後檢討 / 檢討會 |
| Thermal Management | Controlling temperatures in hardware components | 散熱管理 |
| Qualitative vs Quantitative | Opinion-based vs. Data-based arguments | 定性與定量 |
