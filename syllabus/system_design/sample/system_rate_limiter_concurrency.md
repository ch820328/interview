# System Design Deep Dive: Rate Limiting & Concurrency Control

This document explores the granular details of Rate Limiting algorithms (specifically Token Buckets) and how to safely handle concurrency (Race Conditions) in a distributed environment using Redis.

---

## 1. The Token Bucket Engine (權杖桶演算法)

**Why it wins System Design Interviews:** 
It compresses the memory footprint of tracking millions of users from $O(N)$ (storing arrays of timestamps) down to $O(1)$ (storing just two integers per user).

### Core Mathematical Model
Instead of storing a running log of every request time, we simulate a physical bucket being filled with water tokens at a constant drip rate.

For any given User IP, we only need to store **two variables** in our Database/Cache:
1. `current_tokens` (Int): How many tokens are in the bucket right now.
2. `last_refill_timestamp` (Float): The exact Epoch time the bucket was last updated.

### The Pseudo-Logic (Execution Flow)
When a request arrives at $T_{now}$:
1. **Calculate time elapsed:** `delta = T_now - last_refill_timestamp`
2. **Calculate new tokens generated:** `generated_tokens = delta * refill_rate_per_second`
3. **Refill Bucket:** `current_tokens = MIN(bucket_capacity, current_tokens + generated_tokens)`
4. **Determine Outcome:**
   - If `current_tokens >= 1`: 
     - Allow Request.
     - `current_tokens -= 1`
     - `last_refill_timestamp = T_now`
     - Save to DB.
   - If `current_tokens < 1`:
     - Reject Request (HTTP 429).
     - Do not update the `last_refill_timestamp` (bucket remains empty).

---

## 2. Distributed Race Conditions (併發的災難)

When you scale from 1 API Gateway to 50 API Gateways, the logic above fails catastrophically under load.

### The Scenario:
User quickly fires 2 duplicate requests.
Gateway A and Gateway B receive them at the exact same millisecond.

1. Gateway A reads Redis: `current_tokens = 1`
2. Gateway B reads Redis: `current_tokens = 1` (It read before Gateway A could save!)
3. Gateway A subtracts 1, saves `0`, and allows the request.
4. Gateway B subtracts 1, saves `0`, and allows the request.

**Result:** A bucket with only 1 token allowed 2 requests to pass. The Rate Limiter is broken.

---

## 3. How NOT to solve it: Distributed Locks (分散式鎖)

The intuitive answer is to lock the Redis row.
*   **Mechanism:** Gateway A acquires a lock (`SETNX my_lock_IP 1`). Gateway B tries to acquire it, fails, and spins (waits). Gateway A reads, calculates, writes, and deletes the lock. Gateway B then proceeds.
*   **Why it's an Anti-Pattern (L5 Red Flag):**
    - **Latency Explosion:** A rate limiter must execute in 1~5ms. Waiting for a network lock to clear can push latency to 50ms+.
    - **Throughput Collapse:** If 100 requests hit simultaneously, 99 are blocked waiting in a queue. Your API Gateway will run out of connection threads and crash before your backend even sees the traffic.

---

## 4. The L5 Solution: Redis Lua Scripts (原子操作)

The industry-standard solution (used by Stripe, AWS, etc.) is to push the mathematical calculation *into* the Redis Server itself, leveraging Redis's single-threaded nature.

### Why Lua?
Redis executes commands using a **Single-Threaded Event Loop**. This means Redis processes exactly *one* command at a time. 
If we send a Lua Script to Redis, Redis guarantees that the entire script will execute from start to finish **atomically**—no other command from any other Gateway can interrupt it.

### The Architecture Shift:
Instead of the Gateway pulling data, calculating, and pushing it back, the Gateway simply says: *"Hey Redis, here is a Lua script. Execute it for this IP and tell me the result."*

```lua
-- Sample Redis Lua Script for Token Bucket
local tokens_key = KEYS[1]
local timestamp_key = KEYS[2]

local rate = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local now = tonumber(ARGV[3])
local requested = tonumber(ARGV[4])

-- 1. Read current state
local last_tokens = tonumber(redis.call("get", tokens_key))
-- If nil, initialize the bucket to full capacity
if last_tokens == nil then
  last_tokens = capacity
end

local last_refreshed = tonumber(redis.call("get", timestamp_key))
if last_refreshed == nil then
  last_refreshed = 0
end

-- 2. Calculate refill
local delta = math.max(0, now - last_refreshed)
local filled_tokens = math.min(capacity, last_tokens + (delta * rate))

-- 3. Determine Outcome (The atomic decision)
local allowed = filled_tokens >= requested

if allowed then
  -- Consume token and save state
  local new_tokens = filled_tokens - requested
  redis.call("set", tokens_key, new_tokens)
  redis.call("set", timestamp_key, now)
  -- Optional: Set EXPIRE to clean up memory
  return { 1, new_tokens } -- 1 means Access Granted
else
  -- Bucket is empty, don't consume, save the refilled state wait for more time
  redis.call("set", tokens_key, filled_tokens)
  redis.call("set", timestamp_key, now)
  return { 0, filled_tokens } -- 0 means Access Denied
end
```

### The Ultimate Benefit
1. **Zero Locking:** No Gateway ever waits for a lock. 
2. **Atomic:** Zero Race Conditions.
3. **Network Optimization:** Instead of passing data back and forth 3 times (`GET`, `CALC`, `SET`), the Gateway makes **1 single network call** (`EVAL script`). This cuts network latency dramatically.
