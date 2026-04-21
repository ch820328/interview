# JWT: Stateless Auth & Security Deep-Dive (JWT：無狀態認證與安全深度解析)

## I. Problem Statement & Nuances (題目與細節)
What is the internal structure of a JWT, and why do we use it instead of traditional Sessions? Explain the trade-offs between statelessness and security (revocation).
JWT 的內部結構是什麼？為什麼我們使用它而非傳統 Session？請解釋無狀態性與安全性（撤銷）之間的權衡。

**Nucleus Insights (核心觀點):**
- **Stateless Verification**: The server doesn't need to store session data in a database/Redis; it verifies the token using a cryptographic key. (伺服器無需存儲 Session，透過密鑰即可驗證。)
- **Self-Contained Payload**: Claims (user ID, permissions) are encoded directly in the token, reducing database round-trips. (聲明直接編碼在 Token 中，減少資料庫查詢。)
- **The "Revocation" Dilemma**: Since tokens are stateless, "logging out" or "banning a user" is difficult without keeping a blacklist. (無狀態特性導致「登出」或「封禁」難以即時實現。)

---

## II. Mechanical Deep-Dive: Structure (底層原理：結構)

A JWT (JWS) consists of three base64url-encoded parts separated by dots:
一個 JWT 由三個部分組成，以點號分隔：

1. **Header (標頭)**: Contains the type (`JWT`) and signing algorithm (`HS256`, `RS256`).
2. **Payload (載荷)**: Contains the **Claims**. Standard claims: `sub` (subject), `exp` (expiration), `iat` (issued at).
3. **Signature (簽名)**: The critical security layer.
   - **Formula**: `Algorithm(Base64(Header) + "." + Base64(Payload), SecretKey)`

---

## III. Quantitative Analysis: HMAC vs RSA (量化指標分析)

**Q:** Which algorithm should you use for a high-performance system?

| Algorithm | Method | Security Level | Best Use Case |
|---|---|---|---|
| **HS256** | Symmetric (One Secret) | Medium | Internal microservices. (內部微服務。) |
| **RS256** | Asymmetric (Public/Private) | **High** | Public APIs, SSO providers. (公開 API、單一登入。) |
| **Performance**| **Fast** | Moderate (CPU intensive) | RS256 is ~10-20x slower than HS256. |

---

## IV. Security & Vulnerabilities (安全性分析)

### 1. The "None" Algorithm Attack
If the header identifies the algorithm as `none`, a naive server might skip signature verification. **Fix**: Never trust the header's algorithm; enforce it in the code. (禁止接受 `none` 演算法。)

### 2. XSS vs CSRF
- **Local Storage**: Vulnerable to **XSS** (Malicious scripts can steal the token).
- **Cookies (HttpOnly)**: Vulnerable to **CSRF** but immune to XSS. (需配合 CSRF Token 使用。)

### 3. Revocation (The Blacklist Pattern)
To instantly invalidate a JWT, you must store its `jti` (unique ID) in a centralized **Redis Blacklist** until it expires. (在 Redis 紀錄黑名單直到過期。)

---

## V. Professional Use Cases (專業使用場景)

| Use Case | Strategy (策略) |
|---|---|
| **Mobile Apps** | Long-lived Refresh Token + Short-lived Access Token. |
| **Microservices** | Edge Gateway verifies JWT, passes user context as headers. |
| **Web Sockets** | Send JWT in the initial handshake; reuse during connection. |

---

## VI. Code: Verification Pattern (Go)

```go
func VerifyToken(tokenString string, secret []byte) (*Claims, error) {
    token, err := jwt.ParseWithClaims(tokenString, &Claims{}, func(t *jwt.Token) (interface{}, error) {
        // Hardcore check: Ensure the algorithm is HMAC before verifying
        if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, fmt.Errorf("unexpected signing method: %v", t.Header["alg"])
        }
        return secret, nil
    })
    // ... handling
}
```

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Claims | 聲明 | Information stored inside the JWT payload. (儲存在載荷中的各項資訊。) |
| Stateless | 無狀態 | The property where each request contains all info needed to process it. (請求包含所有處理所需的資訊。) |
| JTI | JWT ID | A unique identifier for a specific token, used for one-time use or blacklisting. (Token 的唯一辨識碼。) |
| Base64Url | URL 安全編碼 | A variant of Base64 that replaces `+` and `/` to be URL-safe. (更適合用於網址的編碼變體。) |
