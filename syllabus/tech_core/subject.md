# Technical Core — Portfolio Implementation Deep Dive (技術內核索引)

> 本章節專注於履歷中所提到的關鍵核心技術實作、架構選型與自動化流程，強調技術廣度與解決複雜工程問題的能力。

---

## 核心技術文件 (Technical Implementation Guides)

| 檔案 | 內容摘要 | 核心關鍵字 |
|------|---------|-----------|
| [ansible_automation.md](ansible_automation.md) | 高可靠壓力測試環境自動化：結合 Molecule, Dynamic Inventory 與性能優化 | `IaC` `CI/CD` `Ansible` `TDD` |
| [baby_tracker_tech.md](baby_tracker_tech.md) | Offline-First 架構實作：WatermelonDB, LWW 同步機制與 Redis 分佈式鎖 | `Local-First` `Sync` `Redis` `LWW` |
| [redis_technical_deep_dive.md](redis_technical_deep_dive.md) | Redis 專家大師課：從底層數據結構到高可用叢集架構全方位解析 | `Redis` `Cache` `High-Availability` `LUA` |
| [nvssvt_masterclass.md](nvssvt_masterclass.md) | NVIDIA 系統軟體驗證工具包 (NVSSVT)：Grace Hopper 與 MGX 平台驗證大師課 | `NVIDIA` `MGX` `Grace-Hopper` `Validation` |
| [lww_vs_crdt.md](lww_vs_crdt.md) | 衝突解決深度比較：LWW (Last Write Wins) vs. CRDTs 理論與實踐 | `Distributed-Systems` `Consistency` `Sync` |
| [telemetry_and_measurement_agent.md](telemetry_and_measurement_agent.md) | 高精度數據採集層：結合 Hardware Counters, eBPF 與 TPU 遙測技術 | `Observability` `eBPF` `Performance` `TPU` |
| [golang_masterclass.md](golang_masterclass.md) | Go 語言實戰教材：從語法核心到大規模並發工程架構應用 | `Golang` `Concurrency` `Backend` `Gin` |

---

## 指南與規範 (Guidelines)
- [ ] 基礎設施即代碼 (IaC) 規範
- [ ] 性能優化基準測試流程
