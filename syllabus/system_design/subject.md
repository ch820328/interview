# System Design Syllabus — Topic Index (系統設計題庫索引)

> 命名規則：
> - `mock_`: 面試實戰紀錄與模擬題集。
> - `system_`: 底層核心原理、分散式元件深挖與基礎架構設計。

---

## 模擬面試與實戰 (Mock Interviews)
| 檔案 | 題目摘要 |
|------|---------|
| [mock_distributed_message_queue.md](sample/mock_distributed_message_queue.md) | 1M msg/s 分散式訊息隊列 (Kafka-like) |
| [mock_rate_limiter.md](sample/mock_rate_limiter.md) | 分散式限流器設計 (Rate Limiter) |
| [mock_web_crawler.md](sample/mock_web_crawler.md) | 全球級海量網頁爬蟲設計 |
| [mock_notification_service.md](sample/mock_notification_service.md) | 高可用通知系統 |
| [mock_chat_system.md](sample/mock_chat_system.md) | 即時聊天系統設計 |
| [mock_url_shortener.md](sample/mock_url_shortener.md) | URL Shortener 短網址服務 |
| [mock_google_drive.md](sample/mock_google_drive.md) | Google Drive 雲端儲存設計 |

---

## 底層原理與技術指南 (Deep Dives & Guides)
| 檔案 | 內容摘要 |
|------|---------|
| [system_dynamo_architecture.md](sample/system_dynamo_architecture.md) | Dynamo 論文深度解析：一致性哈希與 NWR |
| [system_redis_internals.md](sample/system_redis_internals.md) | Redis 底層原理、動態字串與事件模型 |
| [system_api_and_protocol_design.md](sample/system_api_and_protocol_design.md) | API 設計規範與通訊協定選擇 (gRPC/REST/Websocket) |
| [system_databases_and_storage.md](sample/system_databases_and_storage.md) | 數據庫存儲引擎比較 (LSM-Tree vs B-Tree) |
| [system_distributed_components.md](sample/system_distributed_components.md) | 分散式元件：LB, Cache, MQ 核心權衡 |
| [system_rate_limiter_concurrency.md](sample/system_rate_limiter_concurrency.md) | 限流器併發深度討論 |
| [system_load_balancer.md](sample/system_load_balancer.md) | Load Balancer Guide (負載均衡器核心指南) |
| [system_redis_guide.md](sample/system_redis_guide.md) | Redis Guide (Redis 核心與緩存策略) |
| [system_classic_designs.md](sample/system_classic_designs.md) | 經典架構設計模式與反模式 |
