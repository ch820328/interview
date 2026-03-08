# Behavioral Question: Technical Disagreement (用數據說服主管)

### 🗣️ 面試題目
**"Tell me about a time you disagreed with a technical decision made by a senior engineer or your manager. How did you handle it, and what was the outcome?"**
（請分享一次你與主管或資深工程師在技術決策上發生分歧的經驗。你如何處理？最後結果為何？）

---

### 🌟 實戰 STAR 故事範本 (OCR → OpenCV matchTemplate 案)

#### 1. Situation (情境：問題的背景與嚴重性)
我們有一套 OCR 自動化測試工具，用來截取 BIOS 畫面上的字元判斷測試結果是否正確。當時 BIOS 進行改版後，原有的 ML-based OCR 模型面臨兩個致命問題：
1. **原模型在某些關鍵字元上有誤判率**，且對螢幕偏移 (monitor offset) 非常敏感。
2. **BIOS 新介面的佈局與訓練資料存在 Distribution Shift**，模型準確率大幅下降。

這直接造成自動化測試工具失效，影響到測試流程的交付時程。

#### 2. Task (任務：點出分歧的核心)
主管當時的判斷是：**重新訓練模型來適應新的 BIOS 佈局**，這是最直接的解法，但會導致開發週期延宕數天甚至更長。

我分析了 BIOS 介面的特性後，發現這個問題根本不需要 ML 來解決，使用 ML 是「殺雞用牛刀」。BIOS 介面是**固定解析度、靜態字型佈局**，不需要泛化能力——這正是傳統影像處理最擅長的場景。**我決定提出反對意見。**

#### 3. Action (行動：以原型取代口頭爭論)
我沒有直接開會爭論，因為口頭主張沒有說服力。我選擇先花一天時間建立一個可運行的 Prototype：
- 採用 **OpenCV `matchTemplate`** 進行字元比對。
- 實作 Pre-processing Pipeline，建立涵蓋所有 BIOS 字型的靜態**樣板庫 (Template Library)**。

建立 Prototype 後，我對 500 個歷史測試案例進行 Benchmark，得出以下數據：

| 指標 | 原 ML 模型 | OpenCV matchTemplate (我的方案) |
|---|---|---|
| **準確率** | ~96% | **99.99%** |
| **對螢幕偏移的容忍度** | 差 (敏感) | 佳 (透過座標校正) |
| **交付時間** | 數天〜數週 | **數小時** |
| **後續維護成本** | 高 (重訓模型) | 低 (僅需更換圖片樣板) |

我用這份 Benchmark 報告去找主管，讓**數據替我說話**，而不是意見替我說話。

#### 4. Result (結果：數據化成果與 Learnings)
主管看完 Prototype 與 Benchmark 後，直接採納了我的方案。

最終成果：
- **交付時間：** 從原本預估的數天縮短至數小時
- **準確率：** 穩定達 99.99%（基於 500 案例驗證集，且螢幕偏移容忍度顯著提升）
- **維護成本：** 後續 BIOS 若調整佈局，只需替換樣板圖片，維護成本降低約 80%

**最重要的 Learning：**
> 挑戰已建立的方案時，口頭論證無效——你必須用可運行的原型和可測量的數據來建立討論的基線。讓資料說服人，而非讓觀點說服人。
>
> *"When challenging an established approach, arguments lose to evidence. Build the prototype and let the data speak."*

---

### 💡 面試官點評與 L4/L5 關鍵加分項

1. **「殺雞用牛刀」的技術判斷力：** 識別 ML 對靜態佈局是過度設計，展現了工程師對「用對工具」的敏銳度，而非盲目跟隨 ML 趨勢。
2. **Prototype 優先策略：** 在提出反對前先建立原型，體現了「用行動代替爭論」的 L5 工程師直覺。這比開會爭辯更有效，也不會製造人際衝突。
3. **可量測的 Benchmark：** 不只說「我的方法比較好」，而是提供具體的比較數據（準確率、延遲、維護成本）——面試官最想看到這種 Data-driven 思維。
4. **Learning 聚焦在「人」而非「技術」：** 最終心得是關於如何說服他人、如何推動改變，而不是「OpenCV 比 ML 好」——這才是 Behavioral 面試想考核的軟實力。

---

### ⚠️ 本場面試的關鍵扣分項 (給自己的提醒)

| 問題 | 如何改善 |
|---|---|
| 第一次回答沒有提到「與誰分歧」 | **開頭第一句就點名分歧對象與立場差異** |
| 數字未說明量測方式 | 引用數據時加上量測基礎（「基於 500 個驗證案例」） |
| 需要面試官多次追問才完整 | 事先用 STAR 框架在腦中確認四個元素都齊全再開口 |
| 英文溝通有語法錯誤 | 練習用完整句子口說 STAR，錄音後自我審閱 |

---

### 📝 模範開場白 (面試實戰模板)

> *"My manager wanted to retrain our OCR model to adapt to the new BIOS layout. I disagreed, because the model had a known failure rate on certain characters and was sensitive to monitor offset — problems that retraining wouldn't structurally solve.*
>
> *Instead of arguing, I spent one day building a prototype using OpenCV's `matchTemplate` with a static font template library. I benchmarked it against the retrained-model baseline on 500 test cases: my approach reached 99.99% accuracy versus ~96% for the ML model, and delivered in hours instead of days.*
>
> *The data convinced my manager. We adopted my solution. The key learning: when challenging an established decision, build the thing first and let the numbers speak."*
