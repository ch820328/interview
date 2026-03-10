# Google BQ Behavioral Interview — Story Index (故事庫索引)

> 每新增一個故事，請同步更新本索引。
> **命名規則：** 新故事存到 `sample/` 資料夾，檔名使用 `story_{關鍵字}.md`

---

## 分類說明 (6 大核心類型)

| # | Type | 關鍵評分點 | 對應 Google 維度 |
|---|------|-----------|----------------|
| 1 | **衝突處理與共識對齊** Conflict & Alignment | 同理心、Data-driven、雙贏 | Leadership |
| 2 | **處理模糊性** Handling Ambiguity | 主動性、拆解問題、風險評估 | Googleyness |
| 3 | **領導力與影響力** Leadership & Influence | Ownership、跨團隊、Leading without authority | Leadership |
| 4 | **失敗、反思與韌性** Failure & Resilience | 自我反省、心理韌性、Post-mortem | Googleyness |
| 5 | **優先級與壓力管理** Prioritization & Execution | 決策邏輯、業務判斷、抗壓性 | GCA + Leadership |
| 6 | **Googleyness 文化特質** | 誠信、謙遜、團隊健康 | Googleyness |

---

## 故事庫 (Story Bank)

| 故事檔案 | 故事一句話摘要 | 適用類型 |
|---------|-------------|---------|
| [story_ocr_opencv.md](sample/story_ocr_opencv.md) | BIOS 改版後，以 24hr PoC + 三方會議說服主管/ML/QA，誤判率降低 100 倍，每週節省 40 小時 | `T1` `T3` `T5` |
| [story_flaky_tests.md](sample/story_flaky_tests.md) | Flaky Test 30%→5%：說服主管的 ROI Matrix + Registry Pattern 治理 + 1-on-1 收服反對者 | `T1` `T2` `T3` `T4` `T6` |
| [story_bios_bug.md](sample/story_bios_bug.md) | BIOS 環境變數 Bug：召集三方會議，讓產線人員的真實數據打破資深同事的 Sunk Cost 僵局 | `T1` `T3` `T6` |
| [story_bsp_flash.md](sample/story_bsp_flash.md) | BSP Flash 架構改革：PoC + 資安論據說服 PM 與產線，刷機工時降低 50% | `T1` `T3` `T5` |
| [story_portal_migration.md](sample/story_portal_migration.md) | 帶領 30+ 人遷移至集中式 Go/Vue Portal，靠穩定性驅動自願採用，消滅 Configuration Drift | `T2` `T3` `T5` |
| [story_ipc_cost_down.md](sample/story_ipc_cost_down.md) | IPC 規格降級失敗：沒能說服主管預留空間導致現場物理改裝，事後推動 cross-functional NPI 標準 | `T1` `T3` `T4` `T5` |


---

## 類型覆蓋地圖

| Type | 主力故事 | 備用故事 | 狀態 |
|------|---------|---------|------|
| **T1 衝突** | `story_ocr_opencv` | `story_flaky_tests` / `story_bios_bug` / `story_bsp_flash` | ✅ 充足 |
| **T2 模糊性** | `story_flaky_tests` (Layer B) | `story_portal_migration` | ⚠️ 可補強 |
| **T3 領導力** | `story_ocr_opencv` | `story_flaky_tests` / `story_bios_bug` / `story_bsp_flash` / `story_portal_migration` | ✅ 充足 |
| **T4 失敗反思** | `story_ipc_cost_down` | `story_flaky_tests` (失敗線) | ✅ 充足 |
| **T5 優先級** | `story_ocr_opencv` | `story_bsp_flash` / `story_portal_migration` | ✅ 充足 |
| **T6 Googleyness** | `story_flaky_tests` | `story_bios_bug` | ⚠️ 建議補強 |

---

## 優先補強清單

1. ⚠️ **Type 2（模糊性）** — 目前靠 Flaky Tests 的 Layer B 組合，建議補一個更純粹的故事
2. ⚠️ **Type 6（Googleyness）** — 缺少「犧牲個人利益 / D&I」主線故事

---

## 新增故事命名規則

```
sample/story_{關鍵字}.md
```

每個故事檔案內必須包含：
- `適用題型` 標籤（T1~T6）
- `核心事實` 表格（數字不變）
- `切角開場白` 區塊（每個 Type 一個版本）
- `完整 STAR`
- `關鍵扣分提醒`
