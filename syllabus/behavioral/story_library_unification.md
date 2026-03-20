# Technical Disagreement: Library Unification (技術分歧：函式庫統一化)

## Question (面試問題)
**Tell me about a time you had a significant technical disagreement with a colleague. How did you handle it, and what was the outcome?**
**請分享一次你與同事在技術上產生重大分歧的經驗。你如何處理這種情況，結果又是如何？**

---

## Model Answer Opening (範例回答開場)
"I'd like to share an experience where I challenged a standard practice to improve systemic stability. We were facing a 10% test failure rate due to library class overrides. While my lead proposed a localized 're-initialization' fix, I argued for a full unification of our core libraries to solve the root cause. By presenting data on CI efficiency and offering to take on the long-term maintenance, I reached a consensus that removed 30,000 lines of technical debt."
「我想分享一次我挑戰現有慣例以提升系統穩定性的經驗。當時我們面臨 10% 的測試失敗率，主因是函式庫類別被覆寫。雖然我的主管提議使用區域性的『重新初始化』來修復，但我主張應全面統一核心函式庫以解決根本問題。透過提出 CI 效率數據並承諾承擔長期維護責任，我最終達成共識，並移除了 3 萬行技術債。」

---

## STAR Narrative (STAR 故事敘述)

**Situation (情境):**
Approximately 10% of our automated test failures were caused by library class collisions. Different developers were creating their own local versions of core tools (IPMI, OCR, etc.), which would occasionally override the common library, leading to unpredictable behavior and "flaky" results.
大約有 10% 的自動化測試失敗是由於函式庫類別衝突引起的。不同的開發人員為核心工具（如 IPMI、OCR 等）創建了自己的區域版本，這些版本偶爾會覆寫公共函式庫，導致不可預測的行為和「不穩定」的結果。

**Task (任務):**
My goal was to stabilize the testing environment and eliminate the culture of fragmented code. The challenge was that my supervisor preferred a safer, less intrusive fix of just re-initializing the environment before each test.
我的目標是穩定測試環境並消除程式碼片段化的文化。挑戰在於，我的主管更傾向於一種較不具侵入性、較穩健的修復方式，即在每次測試前重新初始化環境。

**Action (行動):**
1. **Data Collection:** I calculated the ROI. Re-initializing before each of the 200+ tests would add ~1 minute per test, totaling over 3 hours of extra CI time daily.
   **數據收集：** 我計算了投資報酬率。在 200 多個測試中的每一個之前進行重新初始化，每次會增加約 1 分鐘，每天總計增加超過 3 小時的 CI 時間。
2. **Technical Leadership:** I developed 10+ core classes (IPMI, Windows API, OCR API) to provide a superior, unified alternative.
   **技術領導力：** 我開發了 10 多個核心類別（IPMI、Windows API、OCR API），以提供更優質、統一的替代方案。
3. **Accountability:** I added comprehensive unit tests to the new common library and committed to being the long-term maintainer to reduce the burden on other teams.
   **承擔責任：** 我在新的公共函式庫中加入了全面的單元測試，並承諾擔任長期維護者，以減輕其他團隊的負擔。

**Result (結果):**
The supervisor agreed with the data-driven proposal. We successfully removed nearly 30,000 lines of redundant code. The test failure rate due to collisions dropped to 0%, and CI efficiency remained high.
主管同意了這項以數據驅動的提議。我們成功移除了近 3 萬行冗餘程式碼。因衝突導致的測試失敗率降至 0%，且 CI 效率保持高效。

---

## Impact & Data Table (影響與數據表)

| Metric (指標) | Before (之前) | After (之後) | Impact (影響) |
|---|---|---|---|
| **CI Time Delay (CI 時間延遲)** | +3.3 hours (Projected) | 0 hours added | Saved 3+ hours per run (節省 3+ 小時) |
| **Code Volume (程式碼量)** | High Redundancy | -30,000 lines | Reduced Maintenance (降低維護成本) |
| **Collision Failure Rate (衝突失敗率)** | 10% | 0% | High Reliability (高可靠性) |

---

## L4 Scoring Notes (L4 評分重點)

- **Ownership (所有權):** Proactively took charge of the 30k line deletion and offered long-term support. (主動承擔 3 萬行代碼刪除並提供長期支持。)
- **Influence (影響力):** Used data (CI time) instead of authority to persuade a senior lead. (使用數據而非權威來說服資深主管。)
- **Complexity (複雜性):** Managed a transition involving 10+ different technology domains (IPMI to OCR). (處理涉及 10 多個不同技術領域的遷移。)

---

## Evaluation Rubric (評估量表)

| Criterion (準則) | Rating (評等) | Notes (備註) |
|---|---|---|
| **Conflict Resolution (衝突解決)** | Strong Hire | Effectively used data-driven persuasion. (有效使用數據驅動的說服力。) |
| **Technical Vision (技術願景)** | Strong Hire | Identified root cause vs quick fix. (識別根本原因而非權宜之計。) |
| **Stakeholder Management (利益相關者管理)** | Hire | Reduced "maintenance pain" to gain buy-in. (透過降低「維護痛苦」來獲得認同。) |

---

## Technical Term Dictionary (技術術語表)

| Term (術語) | English Definition | Chinese Translation (中文翻譯) |
|---|---|---|
| **ROI (Return on Investment)** | The ratio of benefit relative to the cost of an investment. | **投資報酬率**：投資收益相對於成本的比率。 |
| **Flaky Test** | A test that yields both passing and failing results with the same code. | **不穩定測試**：在相同代碼下既會通過也會失敗的測試。 |
| **CI/CD Pipeline** | Automated sequence of steps to build, test, and deploy code. | **CI/CD 流水線**：建立、測試和部署代碼的自動化步驟序列。 |
| **Redundant Code** | Source code in a program which is unnecessary. | **冗餘程式碼**：程式中不必要的原始碼。 |

Syllabus saved to: `/home/interview/syllabus/behavioral/story_library_unification.md`
Syllabus 已儲存至：`/home/interview/syllabus/behavioral/story_library_unification.md`
