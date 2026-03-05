# System Design Mock Interview Sample: Google Drive

**Target Level:** Google L4 / L5 (Senior Software Engineer)
**Focus Area:** Distributed Storage, Data Sync, API Design, System Bottlenecks

---

## 1. Requirements Gathering (Functional & Non-Functional)

**Functional Requirements:**
1. Users can upload and download files from any device.
2. Files are synchronized automatically across multiple devices (e.g., laptop updates are visible on mobile).
3. Users can share files with other users (Scoping out real-time collaborative editing for this specific 45-min interview).

**Non-Functional Requirements (CAP Theorem Focus):**
- **Candidate's Initial Intuition (AP):** Chose Availability and Partition Tolerance because users need fast access from their local regions.
- **Interviewer's Challenge & L5 Correction (Split CAP Approach):** 
  - Entirely classifying Google Drive as AP is dangerous.
  - **File Data (Blobs):** Can lean toward Highly Available (AP) using regional edge servers and CDNs.
  - **Metadata (File names, folder tree, permissions):** Must be Strongly Consistent (CP) using a database like Google Spanner (or SQL with strict consistency guarantees). Without CP for metadata, offline syncs would result in catastrophic folder structure corruption and orphaned files.

## 2. Capacity Estimation (Back-of-the-Envelope)
- **Assumptions:** 50 Million Daily Active Users (DAU), uploading 2 files/day, average size 500 KB (rounded to 1 MB/day per user for math ease).
- **Daily Storage:** 50,000,000 * 1 MB = 50 TB / day.
- **5-Year Trajectory:** 50 TB * 365 days * 5 years ≈ 91 PB.
- **Conclusion:** 100 PB requires highly scalable Object Storage (e.g., AWS S3, Google Cloud Storage) and precludes storing file blobs directly in relational databases.

## 3. API Design & High-Level Architecture
**Bottleneck Addressed:** Large file uploads (e.g., 500 MB video) dropping at 99%.

### Chunking & Resumable Uploads
- **Candidate Proposal:** Split files into 100MB chunks and use checkpoints.
- **Standard Practice (L5):** Files are usually chunked much smaller (5MB - 8MB). Clients maintain a cursor. If the network drops, the client queries the server for the last acknowledged chunk offset and resumes seamlessly (Resumable Upload).

### The Presigned URL Architecture (Avoiding Server OOM)
- **Candidate Intuition:** Upload chunks to the server.
- **Interviewer Correction (The L5 Trap):** Uploading large binaries directly through the Application Server (API Gateway) will exhaust network bandwidth and crash the servers (OOM) under heavy concurrent load. 
- **The Solution:** 
  1. Client hits App Server for an upload ticket.
  2. App Server validates permissions and returns a **Presigned URL (Signed URL)** directly linking to the Object Storage.
  3. Client uploads chunks directly to Object Storage, bypassing the App Server.
  4. Object Storage fires an async webhook/event to the App Server upon completion to update the user's Metadata DB.

## 4. Deep Dive: Deduplication (Cost Savings at Scale)
**Bottleneck Addressed:** 10,000 users attempting to upload the exact same viral video. How to avoid saving it 10,000 times?

- **Candidate's Solution (Perfect):** Calculate the **MD5 / SHA-256 Hash**.
- **Execution:** Before requesting the Presigned URL, the client calculates the file's Hash. The App Server checks the Metadata DB. If a file with that Hash already exists in Object Storage, the server returns "Instant Success", creating a metadata pointer to the existing blob without forcing the client to upload any binary data.
- **Bonus:** This Hash acts as a checksum to verify Data Integrity post-upload.

---

## 5. Formal Evaluation Rubric (Mock Result)

*   **Module Completed:** System Design - Google Drive (Storage & Sync)
*   **Target Level:** L4/L5
*   **Overall Rating:** **Hire (H)**

### 👍 Pros / Strengths:
1.  **Engineering Intuition:** Quickly identified the need for Edge Servers, Chunking for network resilience, and Hash-based deduplication.
2.  **Capacity Planning:** Fluent mathematically. Easily navigated the 50M DAU scale to derive a 100 PB 5-year estimate, demonstrating a solid baseline for structural planning.

### 🤔 Cons / Areas for Improvement (Gap to L5 Strong Hire):
1.  **CAP Theorem Depth:** Needs more nuance. An L5 candidate should proactively split the system components (Metadata vs. Blobs) rather than applying a blanket AP/CP label to the whole product.
2.  **Driving the Architecture:** During the upload data flow, an L5 candidate should reflexively defend the App Server by proposing direct-to-storage mechanisms (Presigned URLs) without needing a prompt. Candidates must actively defend API servers from heavy payload abuse.

### 💡 Detailed Justification:
The candidate demonstrates highly stable L4 System Design fundamentals, specifically regarding data transfer resilience and basic capacity scaling. Transitioning to a strict L5 bar requires taking proactive control over disaster scenarios (e.g., caching avalanches, OOM mitigation strategies) and leveraging specific decoupling patterns natively. Excellent learning agility shown when correcting course.
