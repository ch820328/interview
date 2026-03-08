# Behavioral Question: Conflict Resolution (技術分歧與衝突處理)

### 🗣️ 面試題目
**"Tell me about a time when you and another engineer (or your manager) strongly disagreed on a technical decision. How did you handle the conflict, and what was the outcome?"**
（請分享一次你與其他工程師或主管在技術決策上發生強烈分歧的經驗。你如何處理這個衝突？最後的結果是什麼？）

---

### 🌟 實戰 STAR 故事範本 (BIOS 測試工具案)

#### 1. Situation (情境：問題的嚴重性與 Scope)
我們當時負責開發產線測試工具，遇到了一支嚴重的 BIOS Bug。當環境變數超過一定上限時，BIOS 的 Garbage Collection 會異常，導致前面的變數遺失，這直接造成了產線跑測時因為少掉參數而失敗。這是一個會 **Block 產線**的嚴重問題。

#### 2. Task (任務：點出衝突所在)
為了防範這個問題再發生，我們需要開發一個自動化檢測工具。當時一位資深同仁 (Senior Engineer) 主張：先取得 BIOS 當下剩餘的上限空間，然後寫入 `90% Size` 去測試會不會遺失。
但他已經把這套邏輯實作完了。我拿到 Code Review 時，**我提出了強烈的不同意 (Strong Disagreement)**。

#### 3. Action (行動：展現技術直覺、同理心與 Leadership)
我反對的理由是：『測試的目的是為了保證產線能順利運行，而不是極限測試 BIOS。』用 90% 去壓測不僅不符合真實 Scenario，還可能因為未知的邊界效應引發 False Alarm (誤報)，反而會拖累產線良率。我的主張是：**應該先拉出產線實際需要的變數數量底線，再乘上一個安全係數去測試空間是否足夠。**

由於那位同仁堅持不用改（因為他已經寫完了，有沉沒成本），而這個決策會影響到良率。於是，我**沒有直接否定他，而是主動發起了一場 Sync-up Meeting**。
我把我們的直屬主管、BIOS RD 負責人、QA 以及產線人員全部邀請進來。在會議上，我：
1. 先釐清了 Issue 剛爆發時的 Root Cause。
2. 讓產線人員親自說明他們真實在用的變數數量大約是多少。
3. 透過**實際數據與各方需求**，讓大家把焦點從『誰的 Code 寫得好』拉回到『我們真正要解決的 Business Goal 是什麼』。

#### 4. Result (結果：數據化的成果與 Learnings)
經過那次會議，各方達成共識：極限測試不符合產線需求。
最後我們決定採取我的方案：重新實作測試邏輯，確保 BIOS 只要有足夠空間儲存 `200 個` 環境變數即算 Pass。
這不僅**解決了這波 BIOS Bug 引發的產線阻塞問題**，也**避免了未來因為過度測試而造成的 False Alarm**。更棒的是，這次經驗讓我體會到，在發生技術分歧時，把『終端使用者（在這裡是產線人員）』拉進來一起看數據討論，往往能最快打破工程師彼此間的盲點與僵局。

---

### 💡 面試官點評與 L4/L5 關鍵加分項
1. **Testing Philosophy (測試哲學)**: 強調了 False Alarm 的風險，展現不只是會寫 Test，更懂得何謂「有效測試」。
2. **Initiative & Ownership**: 把找主管介入，包裝成「主動牽頭組織一次跨部門溝通會議」。
3. **Data-driven vs Ego**: 面對衝突與沉沒成本，選擇把商業目標與數據攤開來看，成功化解僵局。
