# Story: 樹莓派截圖工具重構 (深入底層解決無人管的 OCR 測試不穩)

**適用題型 (Applicable Types):**
`✅ Type 6 Googleyness (承擔爛攤子/Owner Mindset)` `✅ Type 4 失敗與反思 (系統不穩定的根因探究)` `✅ Type 2 模糊性 (定位未知的不穩定來源)`

---

## 🔑 核心事實（不變）

| 項目 | 內容 |
|---|---|
| **專案背景** | 樹莓派上運行多種測試輔助服務 (GPIO, HID, USB KeyEmulator, 截圖)。其中截圖功能被大量用於 OCR 自動化測試。 |
| **痛點與爛攤子** | 舊截圖程式採「單次啟動 IO」架構。在最差的 Pi 設備上，每截 3 張圖必定失敗 1 次。這會導致測試中斷，QA 需耗費 20 分鐘重新前置準備，每次失敗額外浪費 30 分鐘人力。 |
| **無人接管的原因** | 該工具屬歷史遺留代碼，且運作在樹莓派底層，大家都當作「環境問題」而沒人想去深究重構。 |
| **技術選型決策** | 評估了 Go 與 Rust。因部分設備仍是老舊的 Pi 3，Go 的 GC 與 Runtime 負載過高，最終選擇性能與底層控制極佳、且無 GC 開銷的 Rust 進行重構。 |
| **影響力與推動** | 主動尋找最容易出錯的設備做 PoC (概念驗證)。展示了 CPU 使用率下降 50%、截圖速度從 2.5 秒大幅縮短至 0.2 秒的驚人數據，成功說服主管正式導入。 |
| **高效率開發 (Resourcefulness)** | 為了不在滿檔的 KPI 中拖延進度，我先撰寫好技術架構與邏輯規範，接著利用 AI 工作流 (Gemini 等) 加快原型的生成與驗證，幾乎沒有排擠到原本的專案工時。 |
| **韌性設計 (Resilience)** | 引入 Stream 長度維持機制，並加入 Reset Workaround 處理硬體實體斷訊。 |
| **量化成果** | 導入 ECO 測試後，非實體斷訊引發的擷取錯誤完全歸零；單圖擷取速度提升 12.5 倍 (2.5s -> 0.2s)；每次替 QA 省下 30 分鐘的重跑時間。 |

---

## 🎯 切角開場白（依題型換第一句）

### Type 6 — Googleyness (承擔無人管的技術債 / Act like an Owner)
> *"For months, our OCR automated tests were failing randomly. Everyone blamed the test environment or the OCR model, but nobody wanted to dig into the old, unowned Raspberry Pi capture tool that was actually causing it. I decided to stop accepting 'flaky environments' as an excuse."*
>
> **強調重點：**
> - 大家都知道有問題（Flaky），但大家都怪罪「環境」，沒人想管。
> - 主動跨越職責邊界，深入底層挖出 Root Cause（頻繁開關 I/O 導致的硬體 Missing）。
> - 展現了 Google 最看重的 Ownership：把公司的問題當作自己的問題。

---

### Type 4 — 系統除錯與韌性 (Resilience & Deep Dive)
> *"The hardest bugs to fix aren't in your own code; they are in the hardware integration layers written by someone who left the company years ago. Our OCR tests kept failing due to what looked like random hardware disconnects, but I proved it was an architectural flaw in how we handled video streams."*
>
> **強調重點：**
> - 面對看似「随機性 (Random)」的硬體錯誤，不採取重試 (Retry) 的懶惰解法，而是去挖出架構缺陷。
> - 從 High-level 腳本語言下沉到用 Rust 直接操作 `v4l2`。
> - 在新架構中加入保護機制 (Reset Workaround)，承認硬體不完美並透過軟體包容容錯。

---

## 📖 完整 STAR (以 Type 6 承擔爛攤子為主軸)

### Situation（情境）
我們的自動化測試高度依賴掛載在樹莓派上的影像擷取卡，以便將畫面送給 OCR 模型進行判斷。然而，ECO 測試階段的 OCR 成功率一直極度不穩定 (Flaky)。在品質較差的 Pi 設備上，甚至達到「每截 3 張圖必定失敗 1 次」的慘況。這導致測試一中斷，QA 就必須重新花 20 分鐘做前置準備，一次錯誤就是 30 分鐘的人力浪費。多年來，這支舊截圖程式成了沒人願意碰的技術黑洞，大家都把它歸咎於「硬體環境不穩」。

### Task（任務）
這並不是我的 KPI，我也不是這個截圖工具的 Owner。但我意識到，如果底層的截圖訊號不穩，上面再怎麼優化自動化腳本都是徒勞。我決定主動當責，消除這個最深的痛點。

### Action（行動）
**1. 找出 Root Cause（拒絕靈異現象）：**
我深入檢視舊代碼，發現它採用的是非常暴力的「單次開關」架構：每次呼叫截圖，就啟動 I/O 擷取訊號並輸出最後一幀然後關閉。這種頻繁的 I/O Trigger 直接導致了硬體層級的 Device Missing。這不是環境問題，而是架構設計的缺陷。

**2. 技術選型與高效落實 (Go vs Rust & AI Multiplier)：**
我決定採用直接操作 `v4l2` 的持續串流 (Stream) 架構。在語言選型上，我最初也是考慮 Go 與 Rust。但因為團隊中仍有老舊的樹莓派 3，Go 的 GC 與 Runtime 對老設備的負載太高，因此最終選擇了無 GC 成本、底層控制力極強的 **Rust**。
為了不想讓這個「業餘專案」拖累我原本的 KPI，我撰寫了清楚的技術架構與 API 規範後，利用 AI 工具 (Gemini) 輔助生成基礎原型與進行驗證，這讓我以極小的工時完成了原本需要耗費一兩週的底層重構。

**3. 證明價值與容錯設計 (PoC to Manager)：**
我沒有強制大家立刻轉換。我主動把這套新系統部署在「最容易掛掉的 Pi」上做 PoC，並向主管展示 Demo：CPU 使用率下降了 50% 以上，單張截圖更是從 2.5 秒壓縮到了 0.2 秒。同時我在程式內放入 Reset Workaround 自動應對真實的斷訊。主管看到這壓倒性的數據後，立刻同意導入整個測試產線。

### Result（結果）
- ✅ **故障率歸零：** 導入 ECO 測試後，除了設備實體斷訊外，原本「每截 3 張掛 1 張」的軟體 Flaky Test 完全消失。
- ✅ **測試產能解放：** 單次截圖速度提升 12.5 倍 (2.5s -> 0.2s)；更重要的是，徹底消滅了 QA 每次遇到當機所需浪費的 30 分鐘復原工時。
- ✅ **展現影響力：** 我成功將一個被團隊視為「不可控的硬體玄學問題」，轉變成一套高效、穩定且不佔用過多開發工時的系統底層服務。

**Learning:** 面對系統的不穩定，最危險的心態就是把它歸咎於「環境變數」。真正的 Owner 會一路向下挖（甚至挖到 Linux 驅動層），直到證明它是一個可以被軟體修補的工程問題。

---

## ⚠️ 關鍵扣分提醒 (Critical Pitfalls)

| 常見錯誤 (Common Bugs) | 正確做法 (Fix) |
|---|---|
| 對為什麼用 Rust 解釋不清 | 必須提出 **技術權衡 (Trade-off)**：「因為有老舊的 Pi 3，所以放棄了有 GC 的 Go，選擇開銷更低的 Rust。」這句話含金量極高。 |
| 沒有強調這是一個「沒人管的爛攤子」 | 面試官非常愛追問 "Did someone assign this to you?"，你必須回答 "Nobody. I just couldn't stand the 30-minute productivity loss everyone was accepting as normal." |
| 沒有量化數據或比較基準 | 直接開出數字殺手鐧：「截圖時間從 2.5s -> 0.2s，CPU 下降 50%，把最差的機器變成最穩定的機器。」 |
| 刻意隱瞞使用 AI 寫 Code | 在 Google，AI 是生產力工具。主動提到「我梳理好 Architecture，然後用 AI 加速 prototyping」，會被認為是 Resourceful (善用資源) 且沒有浪費公司時間去填海的 Smart Engineer。 |
