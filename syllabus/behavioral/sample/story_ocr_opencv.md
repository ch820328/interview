# Story: OCR → OpenCV（BIOS 測試工具改版）

**適用題型 (Applicable Types):**
`✅ Type 1 衝突` `✅ Type 3 領導力` `✅ Type 5 優先級`

---

## 🔑 核心事實（不管怎麼問，這些數字/動作不變）

| 項目 | 內容 |
|---|---|
| **背景** | BIOS 改版後，ML OCR 模型誤判率飆升，QA 需手動複查，每次 Build 耗 2 小時 |
| **主管立場** | 重新訓練模型（需數天〜數週）|
| **ML 工程師立場** | 維持架構一致性，不引入 OpenCV |
| **我的方案** | OpenCV `matchTemplate` + 靜態樣板庫 |
| **PoC 時間** | 24 小時建 Prototype |
| **Benchmark 基礎** | 500 個歷史測試案例 |
| **準確率** | ML ~99% → OpenCV 99.99%（誤判率降低 100 倍）|
| **業務影響** | 每週節省 40+ 小時 QA 人力；BIOS 交付週期縮短 20%；解除 CI/CD 阻塞 |
| **ML 工程師處理** | 邀請他擔任 Reviewer，讓他從反對者變成技術把關者 |
| **主管溝通方式** | 會後私下 1-on-1，承諾若 PoC 數據不好就全力配合重訓 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 1 — 衝突處理 (Conflict & Alignment)
> *"My manager and I had a direct technical disagreement — he wanted to retrain the OCR model, and I believed that was the wrong tool for a static, fixed-resolution environment like BIOS menus. Here's how I navigated that conflict."*

**強調重點：**
- 分歧的本質（ML 重訓 vs. 靜態比對）
- 會後私下找主管 + PoC 承諾（建設性反對）
- 數據說服，讓數據替我說話而不是意見

---

### Type 3 — 領導力與影響力 (Leadership & Influence)
> *"Three teams — QA, ML, and my manager — had three different definitions of 'solved,' and they were in direct conflict. Nobody asked me to bridge that gap. I decided to."*

**強調重點：**
- 主動識別三方資訊不對稱
- 邀請 ML 工程師擔任 Reviewer（把對手變盟友）
- 自己主持三方同步會議，無職銜授權

---

### Type 5 — 優先級與壓力管理 (Prioritization & Execution)
> *"QA was completely blocked. Retraining would take weeks. I had 24 hours to prove there was a faster path — or we'd lose the release window."*

**強調重點：**
- QA 急迫性 vs. 架構完美性的 Trade-off
- 24 小時 PoC 決策邏輯
- 結果：一周內完善工具，未延誤交付

---

## 📖 完整 STAR（最完整版本，口說時依題型選擇前半段重點）

### Situation（情境）
BIOS 主版本升級後，我們的 OCR 自動化測試工具因介面 Distribution Shift 出現嚴重誤判，QA 每次 Build 需額外 2 小時手動複查。三方有三種不同的「解決」定義：
- **QA：** 速度優先，今天就要能動
- **ML 工程師：** 架構一致性，不引入第二套影像庫
- **主管：** 可預測性，傾向用既有 ML 資源

### Task（任務）
我意識到自己是三方的天然橋梁。目標：立刻解除 QA 阻塞，同時獲得主管與 ML 工程師的認可，不製造長期技術債。

### Action（行動）
**1. 建設性反對（會中 → 會後）：**
Engineering meeting 中，主管提出重訓模型時，我先認可泛化能力的重要性，然後提問：「針對 BIOS 這種固定解析度的靜態場景，重訓是否路徑最短？」我沒有在會議上繼續爭辯，而是會後私下找主管，承諾：「若 PoC 數據不好，我全力配合重訓。」

**2. 24 小時 PoC：**
用 OpenCV `matchTemplate` + 靜態字型樣板庫建立 Prototype，在 500 個歷史案例上 Benchmark。

**3. 化解 ML 工程師阻力：**
他在三方會議中提出 OpenCV 無法應對未來 UI 變更。我的回應不是反駁，而是**邀請他擔任 Reviewer**，並說：「這是針對 BIOS 靜態場景的專項優化，不是取代你的 ML 框架。」我將程式碼模組化讓他審閱 API，他從反對轉為技術把關。

**4. 主持三方同步會議：**
展示並列比較表（準確率、交付時間、維護成本），用數據取代意見。

### Result（結果）
| 指標 | 前 | 後 |
|---|---|---|
| OCR 準確率 | ~99% | 99.99%（誤判率 ↓100x）|
| 每次 Build 手動工時 | 4 小時 | 0 小時 |
| 每週節省工時 | — | 40+ 小時 |
| BIOS 交付週期 | 兩天一版 | 一天一版（↓20%）|
| CI/CD 阻塞 | 是 | 解除 ✅ |

**Learning:** 對齊的本質不是贏得爭論，而是讓原本被取代的人在解決方案中找到自己的角色。

---

## ⚠️ 關鍵扣分提醒

| 常見錯誤 | 正確做法 |
|---|---|
| 第一次回答沒有點明「三方衝突」 | 第一句話就點出「三方，三種定義，直接衝突」 |
| 沒提主管私下溝通的細節 | 主動說明「我在會後私下找主管，保全他的權威」 |
| 業務影響只說「準確率提升」 | 必須說「40 小時/週」「20% 週期縮短」「CI/CD 解封」 |
| 等面試官追問才補完整 | STAR 第一次講就要包含全部四個要素 |
