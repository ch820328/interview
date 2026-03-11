# Google BQ Behavioral Interview — Story Index (故事庫索引)

> 每新增一個故事，請同步更新本索引。
> **命名規則：** 新故事存到 `sample/` 資料夾，檔名使用 `story_{關鍵字}.md`

---

## 分類說明 (7 大核心類型 - 針對 L4 優化)

| # | Type | 關鍵評分點 | 對應 Google 維度 |
|---|------|-----------|----------------|
| 1 | **衝突處理與共識對齊** Conflict & Alignment | 同理心、Data-driven、雙贏 | Leadership |
| 2 | **處理模糊性** Handling Ambiguity | 主動性、拆解問題、風險評估 | Googleyness |
| 3 | **領導力與無權威影響力** Leadership & Influence | 跨團隊、Leading without authority | Leadership |
| 4 | **失敗、反思與韌性** Failure & Resilience | 自我反省、心理韌性、Post-mortem | Googleyness |
| 5 | **優先級與壓力管理** Prioritization & Execution | 決策邏輯、業務判斷、抗壓性 | GCA + Leadership |
| 6 | **Googleyness (特化：Mentorship/爛攤子)** | 指導新人、主動承擔未被分配的技術債 | Googleyness |
| 7 | **技術難題與權衡** Technical Trade-offs | 交付速度 vs 程式碼品質、處理技術債 | GCA + Tech |

---

## 故事庫 (Story Bank)

| 故事檔案 | 故事一句話摘要 | 適用類型 |
|---------|-------------|---------|
| [story_ocr_opencv.md](sample/story_ocr_opencv.md) | BIOS 改版後，以 24hr PoC + 三方會議說服主管/ML/QA，誤判率降低 100 倍，每週節省 40 小時 | `T1` `T3` `T5` |
| [story_flaky_tests.md](sample/story_flaky_tests.md) | Flaky Test 30%→5%：說服主管的 ROI Matrix + Registry Pattern 治理 + 1-on-1 收服反對者 | `T1` `T2` `T3` `T4` `T6` |
| [story_bios_bug.md](sample/story_bios_bug.md) | BIOS 環境變數 Bug：召集三方會議，讓產線人員的真實數據打破資深同事的 Sunk Cost 僵局 | `T1` `T3` `T6` |
| [story_bsp_flash.md](sample/story_bsp_flash.md) | BSP Flash 架構改革：PoC + 資安論據說服 PM 與產線，刷機工時降低 50% | `T1` `T3` `T5` |
| [story_portal_migration.md](sample/story_portal_migration.md) | 帶領 30+ 人遷移至集中式 Go/Vue Portal，靠穩定性驅動自願採用，消滅 Configuration Drift | `T2` `T3` `T5` `T7` |
| [story_ipc_cost_down.md](sample/story_ipc_cost_down.md) | IPC 規格降級失敗：沒能說服主管預留空間導致現場物理改裝，事後推動 cross-functional NPI 標準 | `T1` `T3` `T4` `T5` `T7` |
| [story_bios_security_notification.md](sample/story_bios_security_notification.md) | 從一句話需求到梳理跨國API依賴，利用時程透明化說服PM等待6週ETA，實作半自動化寄信系統 | `T1` `T2` `T3` `T5` |
| [story_test_library_mentorship.md](sample/story_test_library_mentorship.md) | 解決新人迷航痛點：主動將異質測試工具封裝成共用 Library 並建立 API 文件庫，加速 Onboarding | `T2` `T3` `T6` |
| [story_raspberry_pi_rust_capture.md](sample/story_raspberry_pi_rust_capture.md) | 承接無人管的歷史爛攤子：用 Rust 底層直連 v4l2 重構樹莓派截圖架構，修復 90% 的 OCR Flaky Tests | `T2` `T4` `T6` |
| [story_jetson_bsp_tradeoff.md](sample/story_jetson_bsp_tradeoff.md) | 克服過度工程的誘惑：在 Jetson BSP 編譯流程中放棄軟體解耦，改用實體機暴力綁定，換取未來的零維護成本 | `T4` `T5` `T7` |


---

## 類型覆蓋地圖

| Type | 主力故事 | 備用故事 | 狀態 |
|------|---------|---------|------|
| **T1 衝突** | `story_ocr_opencv` | `story_bios_security_notification` / `story_flaky_tests` / `story_bios_bug` / `story_bsp_flash` | ✅ 充足 |
| **T2 模糊性** | `story_bios_security_notification` | `story_flaky_tests` (Layer B) / `story_portal_migration` | ✅ 充足 |
| **T3 影響力(無權威)** | `story_ocr_opencv` | `story_bios_security_notification` / `story_flaky_tests` / `story_bios_bug` / `story_bsp_flash` / `story_portal_migration` | ✅ 充足 |
| **T4 失敗反思(除錯)** | `story_ipc_cost_down` | `story_raspberry_pi_rust_capture` / `story_flaky_tests` / `story_jetson_bsp_tradeoff` | ✅ 充足 |
| **T5 優先級(權衡)** | `story_ocr_opencv` | `story_bsp_flash` / `story_portal_migration` / `story_jetson_bsp_tradeoff` | ✅ 充足滿分 |
| **T6 Googleyness** | `story_raspberry_pi_rust_capture` | `story_test_library_mentorship` / `story_flaky_tests` | ✅ 充足滿分 |
| **T7 技術權衡**| `story_jetson_bsp_tradeoff` | `story_ipc_cost_down` / `story_portal_migration` | ✅ 充足滿分 |

---

## 優先補強清單

1. ✅ **Type 2（模糊性）** — 已用 `story_bios_security_notification` 作為主線故事補充。
2. ✅ **Type 6（Googleyness）** — 已透過 `story_test_library_mentorship` (指導新人) 與 `story_raspberry_pi_rust_capture` (處理無人管的技術債) 達成 100% 完整涵蓋。
3. ✅ **Type 7（技術權衡）** — 已透過 `story_jetson_bsp_tradeoff` (妥協工程完美度換取維護性) 補上最後一塊拼圖。

🎉 **目前 L4 BQ syllabus 已經 100% 覆蓋所有重要題型！**

---

## 新增故事命名規則

```
sample/story_{關鍵字}.md
```

每個故事檔案內必須包含：
- `適用題型` 標籤（T1~T7）
- `核心事實` 表格（數字不變）
- `切角開場白` 區塊（每個 Type 一個版本）
- `完整 STAR`
- `關鍵扣分提醒`
