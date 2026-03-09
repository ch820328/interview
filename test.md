為了修正你提到的「跟進回答過於簡短」與「跳過基礎解法」的問題，下次練習時，我們強制使用以下 「回應腳本結構」：

Coding 階段的強制結構：
Clarify: Ask 2-3 questions about constraints.

Brute Force: "A naive approach would be [X], which takes O(n^2). This is useful for [Y] but fails at [Z]."

Optimal Approach: "To optimize, we can use [Data Structure] to reduce this to O(n) because [Reason]."

Complexity: "This solution gives O(n) time and O(n) space."

Implementation: Start coding (Sync with verbal explanation).

System Design 階段的強制結構：
Requirements: List Functional & Non-Functional.

Scale: State QPS and Storage (The "Capacity Estimation").

High-Level Design: Draw the components, then explain "Data Flow."

Deep Dive: Focus on 1-2 bottlenecks (e.g., Latency, Scaling).

Trade-offs: "I chose A over B because [Justification]."