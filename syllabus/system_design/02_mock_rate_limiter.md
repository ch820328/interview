# System Design Mock Interview Sample: Rate Limiter

**Target Level:** Google L4 / L5 (Senior Software Engineer)
**Focus Area:** API Protection, Memory Compression, Redis, Concurrency Control (Race Conditions)

---

## 1. Requirements Gathering & API Scope

**Functional Requirements:**
1. Limit API request counts for users / IP addresses (e.g., 100 requests per minute).
2. Protect against both malicious DDoS bursts and internal accidental microservice retry-loops.
3. Blocked requests must return HTTP 429 (Too Many Requests) immediately at the Gateway, preventing traffic from entering the downstream application tier.
4. Provide a `Retry-After` header telling clients exactly when they are permitted to request again.

**Non-Functional Requirements:**
- **Extreme Low Latency (Critical L5 Requirement):** The Rate Limiter must respond in **1~5 milliseconds**. 
  - *Pitfall:* Proposing 0.1s (100ms) is dangerously slow and will double the latency of the entire backend system. Rate limiters demand In-Memory datastores (like Redis).

---

## 2. Algorithm Deep Dive: Counters vs. Buckets

### Approach A: Fixed Window Counter (Time Block)
- **Concept:** Use a dictionary `IP -> count` set to flush every minute (e.g., 12:00 -> 12:01).
- **The Burst Traffic Edge Case (致命漏洞):** If the limit is 100/min. A user can send 100 requests at 12:00:59, the counter resets at 12:01:00, and they send another 100 requests at 12:01:01. The server receives 200 requests within *two seconds*, completely bypassing the intention of the rate limit.

### Approach B: Sliding Window Log
- **Concept:** Store specific timestamps of every incoming request in an array. Remove timestamps older than 1 minute.
- **The OOM Edge Case:** If a VIP is allowed 1,000,000 requests per minute, saving 1 million timestamps for a single IP consumes megabytes of memory. At scale with millions of IPs, this triggers rapid Out-Of-Memory (OOM) failures in Redis.

### Approach C: Token Bucket (The L5 Standard)
- **Concept:** A bucket holds a maximum number of tokens. Tokens are added to the bucket at a constant rate. Requests consume a token. If the bucket is empty, the request is dropped.
- **The Math & Memory Optimization:** 
  We **do not** need arrays of timestamps. In Redis, we only store:
  1. `current_tokens` (Int)
  2. `last_update_time` (Timestamp)
  When a request arrives, we calculate: `new_tokens = (now - last_update_time) * refill_rate`. Add them to `current_tokens`, subtract 1, update the timestamp, and allow the request. 
  - **Memory:** $O(1)$. Just two integer values per IP constraint.

---

## 3. Distributed Architecture & Race Conditions

**The Scenario:** 50 API Gateways fronting the traffic. A user sends two requests simultaneously to Gateway A and Gateway B within 1 millisecond.
**The Race Condition:** Both check Redis, see 1 token left, both subtract 1, and both allow the traffic. 1 token let 2 requests pass.

### Solution 1: Distributed Locks (Anti-Pattern)
- **Idea:** Gateway A grabs a Redis `SETNX` lock, calculates, and releases.
- **Why it Fails an L5 Interview:** Network I/O ping-pong + lock contention. Locking increases latency from 2ms to 50ms+. Throttled queues will build up, crashing the API Gateway under burst loads.

### Solution 2: Redis Lua Scripting (The Perfect L5 Answer)
- **Idea:** Redis relies on a **Single-Threaded** event loop.
- **Execution:** We write the mathematical logic (checking last time, refilling tokens, taking a token) into a tiny `.lua` script. The API Gateway sends this script + the IP to Redis. Redis executes the script *atomically*.
- **Result:** No Race Conditions. Zero lock contention across network nodes. Lightning-fast execution strictly within RAM.

---

## 📝 Formal Evaluation Rubric (Strict Grading Sample)

*   **Module Completed:** System Design - Rate Limiter (Token Bucket & Concurrency)
*   **Target Level:** L4/L5
*   **Overall Rating:** **Lean Hire (LH)**

### 🤔 Cons / Critical Gaps (Gap to L5 Strict Standards):
1.  **Latency Awareness:** Initially proposed 100ms latency. At Google or Amazon scale, passing every API call through a 100ms tax is an architectural failure. Needs to demonstrate immediate awareness of microsecond/single-digit millisecond budgets for edge-tier security layers.
2.  **Concurrency Blindspot:** Failed to proactively recognize Race Conditions in a multi-gateway scenario. When asked, proposed "locks" without recognizing the catastrophic latency implications of Distributed Locks on an edge Gateway. At the L5 level, proposing Lua Scripts or Redis Atomic pipelines unprompted is heavily expected.

### 💡 Actionable Corrections:
- Do not jump to Distributed Locks to solve concurrency gracefully in latency-critical paths. Study **Redis Single-Threaded properties** and **Atomic Lua Scripts**.
- Study memory footprints. Understand why an array of elements (Sliding Window Log) limits scalability more than mathematically derivable models (Token Bucket / Leaky Bucket).
