# Syllabus: Behavioral Interview (Technical Disagreement / Refactoring)

## 1. Interview Question (EN + ZH)
**English:** Tell me about a time when you and a peer or superior strongly disagreed on a technical decision. How did you handle the situation, and what was the outcome?
**Chinese (Traditional):** 請分享一個你與同事或主管在技術決策上發生強烈分歧的經驗。你如何處理這個情況，最終結果為何？

## 2. Overview of the Candidate's Narrative (STAR)
### Situation / 情境
The test automation framework was plagued by instability ("flaky" tests) due to legacy code causing global variable pollution and unauthorized overrides. This technical debt severely impeded developer velocity.
(自動化測試框架因遺留代碼導致全域變數污染與不可控的覆蓋，造成測試極度不穩定 (Flaky)，這項技術債嚴重阻礙了開發速度。)

### Task / 任務
The candidate proposed a full refactor to migrate custom code into a centralized Common Library. The manager resisted due to the high time cost and risks to the product delivery timeline.
(候選人提議全面重構，將自訂代碼轉移到集中的共用程式庫。但主管因擔憂時間成本與產品交付風險而強烈反對。)

### Action / 行動重點 (Conflict Resolution)
To build consensus and resolve the conflict, the candidate took three critical L4+ actions:
1. **Quantifying the Cost of Inaction (數據化不作為的成本):** Analyzed the past 4 Sprints, proving the team wasted 8-10 hours/week debugging false positives. Projected this to 20 hours/week in 2 months (a 30% drop in release frequency).
2. **Tiered Migration & PoC (風險分層與概念驗證):** Altered the original "full refactor" proposal to an "incremental refactor." Started with the most unstable but least critical module as a Proof of Concept (PoC).
3. **ROI Matrix & Safety Commitment (投資回報與安全承諾):** Presented a 2-week break-even ROI (20 hours to refactor via AI tools vs. 10 hours/week saved). Committed to doing the work outside the main feature budget and promised immediate rollback upon any regression failures.

### Result / 結果
The manager approved the PoC. Over 5,000 lines of high-risk legacy code were successfully removed. Flakiness was significantly reduced, saving the engineering team massive debugging time without impacting product delivery.

## 3. L4/L4+ Scoring Notes
At the L4/L4+ level, engineers must demonstrate that they can balance **technical idealism** with **business reality**. 
- **Business Sensibility:** The candidate successfully converted "technical debt" into a "financial/time loss metric" (10 hours a week lost). This speaks directly to management concerns.
- **Compromise:** The candidate didn't stubbornly insist on a "full refactor." They adapted to a PoC (Proof of Concept) and "incremental migration," which demonstrates maturity.
- **Execution Safety:** The mention of regression suites and immediate rollback plans showed a deep understanding of operational safety.

## 4. Self-Review Deductions Table / 自我檢討扣分表
| Common Pitfalls (常見陷阱) | Did the candidate avoid it? | Feedback (回饋) |
|---|---|---|
| **"I just did it anyway"** (忽視主管直接硬幹) | ✅ Yes | Candidate explicitly sought buy-in via data and negotiation. |
| **"I argued until they agreed"** (純靠技術爭辯) | ✅ Yes | Candidate shifted from architectural arguments to ROI/Time metrics. |
| **"We" instead of "I"** (缺乏個人貢獻) | ✅ Yes | "I analyzed", "I proposed a PoC", "I leveraged AI tooling." |

## 5. Model Answer Opening Paragraph (English)
"In my previous project, we had severe technical debt in our automation framework causing flaky tests. I proposed a full refactor, but my manager blocked it due to tight delivery deadlines. To resolve this, I didn't push back on the tech alone; I pulled the data. I showed him that we were already losing 10 hours a week to debugging these false positives. I negotiated a compromise: instead of a full rewrite, I would do a low-risk, incremental Proof of Concept using AI tools to halve my dev time, guaranteeing a 2-week ROI without threatening the current Sprint. He approved the PoC, and it was so successful we eventually retired 5,000 lines of legacy code."

---

## 6. Full Evaluation Rubric (Bilingual)
**Module Completed:** Behavioral - Technical Disagreement
**Overall Rating:** **Strong Hire / 強烈建議錄取**

**Pros / Strengths (優點與強項):**
- **Excellent Consensus Building (卓越的共識建立能力):** Converting technical debt into "Cost of Inaction" (10 hours/week) is exactly how an L4+ engineer should speak to a manager. (將技術債轉換為「不作為成本」，這正是 L4+ 工程師與主管溝通的最佳方式。)
- **De-risking (降低風險的意識):** Pivoting from a massive refactor to a focused Proof of Concept (PoC) showed maturity and business alignment. (主動放棄「全盤重構」，改為提出局部「概念驗證 (PoC)」，展現了成熟度與商業對齊能力。)
- **Clear Framework (清晰的架構):** Your follow-up response deeply mapped to the STAR method and directly answered the prompt regarding negotiation. (後續的回答完美契合 STAR 架構，並直指核心談判技巧。)

**Cons / Critical Gaps to L4/L4+ (缺點與改進空間):**
- **Initial Vagueness (初期的模糊):** Your first answer entirely skipped the *"How did you resolve the disagreement?"* part, jumping straight into coding. If you do this in a real interview, a less proactive interviewer might not prompt you to clarify, and you will fail the behavioral loop. Always lead with the interpersonal resolution when asked about a disagreement. 
  (你最初的回答完全跳過了「如何解決分歧」，直接進入寫程式碼的階段。在真實面試中，如果面試官沒有主動追問，這個行為面試就會被當。當被問到「分歧」時，永遠要把人際溝通與妥協放在首位。)

**Actionable Corrections (可執行的改進建議):**
- **Structure the Conflict Upfront:** When answering "disagreement" questions, explicitly state: 1. The Conflict -> 2. The Negotiation (Data/Compromise) -> 3. The Technical Execution -> 4. The Business Result. Do not hide the negotiation in the middle or wait for a follow-up. 
  (在回答「分歧」題型時，一開始就要明確鋪陳：1. 定義衝突 ➔ 2. 談判與妥協(數據輔助) ➔ 3. 技術執行 ➔ 4. 商業結果。千萬不要等待面試官追問才把談判細節拿出來講。)
