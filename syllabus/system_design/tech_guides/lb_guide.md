# Tech Guide: Load Balancing Strategies (負載平衡策略導引)

**Topic / 主題:** Traffic Distribution & High Availability / 流量分配與高可用性
**Level / 等級:** Google L4 / L5 Standard

---

## 1. Core Concepts (核心概念)

**English:**
A Load Balancer (LB) acts as a "traffic cop" sitting in front of your servers and routing client requests across all servers capable of fulfilling those requests.

**中文：**
負載平衡器 (LB) 充當伺服器前的「交通警察」，將客戶端請求路由到所有具備處理能力的分散式伺服器上。

---

## 2. Types of Load Balancers (負載平衡器類型)

| Layer (層級) | Name (名稱) | Example (範例) | Use Case (使用場景) |
|---|---|---|---|
| **L4** | Transport Layer | Nginx (Stream), AWS NLB | TCP/UDP packet routing. High performance. / 傳輸層路由。 |
| **L7** | Application Layer | Nginx, Envoy, AWS ALB | HTTP/HTTPS routing. Can route by URL path or headers. / 應用層路由，可根據 URL 路徑進行轉發。 |

---

## 3. Implementation Example: Nginx Config (實作範例：Nginx 配置)

**English:** Setting up a Round Robin LB for API Workers.
**中文：** 為 API 工作節點架設輪詢式 (Round Robin) 負載平衡。

```nginx
http {
    upstream backend_servers {
        # Weighted Round Robin
        server 10.0.0.1:8080 weight=3;
        server 10.0.0.2:8080;
        server 10.0.0.3:8080 backup; # Only used if others are down
    }

    server {
        listen 80;
        location /v1/ {
            proxy_pass http://backend_servers;
        }
    }
}
```

---

## 4. Distributed Politeness in Crawlers (爬蟲中的分散式禮貌性實作)

**English:**
In our Web Crawler, the LB ensures that `POST /v1/tasks/complete` requests are distributed across Content Processors based on CPU load.

**中文：**
在網頁爬蟲中，LB 確保 `POST /v1/tasks/complete` 請求根據 CPU 負載分配到不同的內容處理器節點。

---

## 5. L4+ Deep Dive: Health Checks (L4+ 進階：健康檢查)

**English:**
Passive vs. Active Health Checks. At L5, you must discuss how to handle "Gray Failure" where a server is up but responding slowly or with 5xx errors.

**中文：**
被動 vs. 主動健康檢查。在 L5 等級，必須討論如何處理「灰色故障 (Gray Failure)」——即伺服器存活但響應緩慢或持續回報 5xx 錯誤的情況。
