# 🎯 One-Page Prep: Google SWE III (Performance Infra & Automation)

## I. Target Role: Performance Infrastructure & Automation (Taipei)
**Company**: Google | **Level**: SWE III (L4/L5 equivalent focus)

| **Tech Pillars** (核心支柱) | **Infrastructure** (基礎設施) | **Domain Expertise** (領域專長) |
| :--- | :--- | :--- |
| **C++ / Python / Go** | **Test Automation Frameworks** | **Hardware Performance (TPU/GPU/CPU)** |
| **Data Visualization** (Dashboards) | **Regression Testing Pipelines** | **Workload Performance Analysis** |

---

## II. Critical Focus Areas (重點複習領域)

### 1. Performance Measurement High-Fidelity
- **Concepts**: Benchmarking noise, reproducibility, and statistical significance (P99, P95).
- **Deep Dive**: How to isolate OS noise in performance tests?

### 2. HW/SW Co-Design & NPI
- **Focus**: Understanding the lifecycle of **New Product Introduction (NPI)** for TPUs/GPUs.
- **Key**: How would you automate the validation of a new TPU architecture?

### 3. Automated Regression & Triage
- **Algorithm**: Binary Search for regressions (Git Bisect) at scale.
- **System Design**: Designing a dashboard that handles millions of performance data points with real-time visualization.

---

## III. Predicted "Expert Edition" Questions (預測專家級考題)

1. **System Design**: "Design a performance monitoring system for Google’s entire GPU fleet that can detect a 1% regression in throughput within 10 minutes."
2. **Coding**: "Implement a library to calculate moving percentiles (P99) on a high-frequency stream of execution times with minimal memory footprint."
3. **Troubleshooting**: "A TPU benchmark is showing a 5% performance drop, but only on every 10th run. How do you triage this non-deterministic regression?"
4. **Knowledge**: "Explain how NUMA (Non-Uniform Memory Access) architecture impacts the high-fidelity measurement of multi-threaded application performance."
5. **Hardware**: "What are the common bottleneck differences when benchmarks run on a TPU vs. a traditional GPU?"

---

## IV. Dashboard Cheat-Sheet (關聯知識庫)

| Relevant Topic (相關主題) | Focus for this Role (此代辦重點) | Link |
| :--- | :--- | :--- |
| **Goroutines vs Threads** | Understanding context-switch overhead in performance apps. | [View](file:///home/interview/syllabus/questions/Concurrency/goroutines_vs_threads.md) |
| **Resource Management** | Lock contention as a performance bottleneck. | [View](file:///home/interview/syllabus/questions/Concurrency/concurrency_resource_management.md) |
| **Boot Process** | Hardware initialization (SEC/PEI) in NPI cycles. | [View](file:///home/interview/syllabus/questions/System/boot_process.md) |

---

## V. Execution Strategy (執行策略)
- **Phase 1**: Deep dive into **Linux Perf tools** and **Hardware Performance Counters**.
- **Phase 2**: Refine skills in **Statistical Data Analysis** for large-scale telemetry.
- **Phase 3**: Practice System Design with a focus on **Data Visualization & Triage Automation**.
