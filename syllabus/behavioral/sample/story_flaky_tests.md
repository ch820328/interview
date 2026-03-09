# Story: Flaky Tests 治理（測試框架重構 + 工程治理）

**適用題型 (Applicable Types):**
`✅ Type 1 衝突` `✅ Type 2 模糊性` `✅ Type 3 領導力` `✅ Type 4 失敗/反思` `✅ Type 6 Googleyness`

> ⚠️ 這個故事有**兩個層次**，面試時依題型選擇主線：
> - **Layer A（衝突線）：** 說服主管批准增量重構（ROI Matrix）
> - **Layer B（治理線）：** 設計 Registry Pattern + 化解資深同事阻力（EQ）

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **問題** | Flaky Test 比例達 30%+，CI/CD 中隨機失敗，摧毀團隊對自動化的信心 |
| **根本原因** | 各開發者自訂資源類別，無統一生命週期管理，造成 Race Condition |
| **主管障礙** | 主管以交付期限為由，拒絕全面重構提案 |
| **我的解法** | 改為增量重構 PoC，並設計 Registry Pattern 的中央資源管理器 |
| **治理強制手段** | 實作 `pre-commit hook` 攔截未註冊的資源類別 |
| **阻力者** | 一位資深同事，認為 hook 破壞了 DevEx（開發體驗）|
| **EQ 行動** | 主動約他 1-on-1 Pair Programming，根據他的回饋重構底層 API |
| **量化成果** | Flaky Test 30% → 5% 以下；測試執行時間節省 20%；測試環境污染永久消除 |
| **ROI 邏輯** | 每週損失 10 小時 debug；重構僅需 20 小時；2 週回本 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 1 — 衝突（說服主管）
> *"My manager blocked my refactor proposal — not because he was wrong, but because I hadn't spoken his language yet. So I stopped arguing about code quality and started talking about money."*

**強調重點：**
- 初次被拒 → 反思說服框架
- 把「技術債」轉換成「Cost of Inaction」（每週 10 小時損失）
- ROI Matrix：20 小時重構 vs. 10 小時/週損失，2 週回本
- PoC 降風險 + rollback 承諾

---

### Type 2 — 模糊性（無指令下主動治理）
> *"There was no owner, no spec, no one telling me to fix it. The test framework was slowly collapsing — and I decided someone had to be the owner."*

**強調重點：**
- 沒有人指派此任務
- 自行診斷根本原因（Race Condition + 生命週期缺失）
- 主動定義解法（Registry Pattern）並建立治理機制（pre-commit hook）

---

### Type 3 — 領導力（EQ 收服反對者）
> *"I didn't just fix the tests — I built a governance system. And then turned the most vocal critic into its biggest advocate."*

**強調重點：**
- 系統性解法（Registry Pattern）而非一個個修 test
- 資深同事強烈反對 → 約 1-on-1 Pair Programming
- 根據他的回饋重構 API → 他從反對者變成推廣者

---

### Type 4 — 失敗 / 反思
> *"My first move was wrong. I went straight to tech — 'we should refactor this' — and my manager shut it down immediately. That failure taught me how to have conversations that actually land."*

**強調重點：**
- 第一次提案失敗（管理視角缺失）
- 反思：工程師的論點 ≠ 主管的語言
- 行動改變：重新框架為 ROI 與業務損失
- 結果：第二次提案成功，並進一步建立治理機制

---

### Type 6 — Googleyness（謙遜 + 傾聽）
> *"A senior colleague pushed back hard against my new system. It would have been easy to point to my authority as the designer and move on. I didn't."*

**強調重點：**
- 沒有依靠設計者的「權力」壓制
- 主動約 Pair Programming，傾聽對方痛點
- 根據他的反饋真的修改了 API（不是假裝聽）
- 謙遜體現在：接受外部反饋改善自己的設計

---

## 📖 完整 STAR（Layer A + B 合併版）

### Situation（情境）
測試框架規模化後，開發者各自定義資源類別，無統一的測試資源生命週期管理，導致 Race Condition 與全域狀態污染。CI/CD 中的 Flaky Test 比例飆升至 30%+，摧毀了團隊對自動化測試的信心，每週損失 8-10 小時 debug 時間。

### Task（任務）
**Layer A：** 說服主管批准重構，在不影響產品交付時程的前提下推動。
**Layer B：** 從根本上杜絕 Test Pollution，建立工程治理機制。

### Action（行動）
**Layer A — 說服主管：**
1. **量化不作為的成本：** 分析過去 4 個 Sprint，證明每週損失 10 小時，預測 2 個月後損失 20 小時（release 頻率降 30%）
2. **PoC 提案：** 將「全面重構」改為「增量 PoC」，從最不穩定但最不關鍵的模組開始
3. **ROI Matrix + 安全承諾：** 20 小時重構成本 vs. 每週節省 10 小時，2 週回本。承諾若出現 regression 立即 rollback

**Layer B — 建立治理：**
1. **架構設計：** 採用 Registry Pattern，打造中央資源管理器，統一所有測試的 Setup/Teardown 生命週期
2. **強制執行：** 實作 `pre-commit hook` 攔截未註冊的資源類別
3. **化解阻力：** 資深同事強烈抗議 hook 破壞 DevEx → 主動約 1-on-1 Pair Programming → 傾聽他的痛點 → 根據他的回饋重構底層 API → 他從最強反對者變成最強推廣者

### Result（結果）
| 指標 | 前 | 後 |
|---|---|---|
| Flaky Test 比例 | 30%+ | < 5% |
| 每週 Debug 損失 | 10 小時 | 0 |
| 測試初始化時間 | baseline | ↓ 20% |
| Test Pollution | 持續發生 | 永久消除 |

新的中央資源管理器成為工程團隊的 Coding Standard，大幅提升對 CI/CD 的信心。

---

## ⚠️ 關鍵扣分提醒

| 常見錯誤 | 正確做法 |
|---|---|
| 只說「修好了 flaky test」 | 必須說「從根本設計出治理機制，永久杜絕」 |
| 跳過說服主管的過程 | Type 1 題一定要說 ROI Matrix 和主管語言轉換 |
| 沒說資深同事抗拒的細節 | Type 3/6 題必須說 Pair Programming + API 修改 |
| 用「我們」而非「我」 | 「我分析」「我提出」「我主動約」，不要用 we |
