# BIOS & OS Boot Process: Expert Deep-Dive (電腦開機流程與作業系統啟動專家級解析)

## I. Problem Statement & Nuances (題目與細節)
Trace the execution flow from the moment the power button is pressed until the OS login screen appears. What are the critical hand-offs between hardware, firmware, and software?
請追蹤從按下電源鍵到作業系統登入畫面出現的執行流程。硬體、韌體與軟體之間的關鍵交接點為何？

**Nucleus Insights (核心觀點):**
- **The Reset Vector**: The CPU doesn't start at "random"; it hard-jumps to a specific memory address (`0xFFFFFFF0`). (CPU 並非隨機啟動，而是跳轉到特定的重置向量位址。)
- **Transition of Bitness**: The system starts in **16-bit Real Mode** and must transition to **32/64-bit Protected Mode**. (系統從 16 位元實模式啟動，必須轉換到 32/64 位元保護模式。)
- **Chain of Trust**: Each stage must verify the next (Secure Boot). (每一階段都必須驗證下一階段的安全性。)

---

## II. Mechanical Deep-Dive: The 5 Stages of Boot (底層原理：開機五大階段)

1. **POST (Power-On Self-Test)**:
   - BIOS/UEFI initializes the motherboard, CPU, RAM, and essential peripherals (Graphics).
   - BIOS/UEFI 初始化主機板、CPU、記憶體及關鍵周邊（如顯卡）。
2. **Boot Loader Search (尋找啟動程式)**:
   - Firmware looks for a bootable device based on the **Boot Priority**.
   - 韌體根據啟動優先權尋找可啟動裝置。
3. **Primary Boot Loader (MBR/GPT)**:
   - For Legacy: Executes the first 512 bytes (MBR) which contains stage 1 of the bootloader (e.g., GRUB).
   - 傳統模式下執行 MBR 的前 512 位元組，內含啟動程式的第一階段。
4. **Kernel Initialization (內核初始化)**:
   - The bootloader loads the **Kernel Image** (vmlinuz) and **initramfs** into RAM.
   - 啟動程式將內核映像與臨時檔案系統載入記憶體。
5. **System Init (User Space)**:
   - Kernel starts the first process (`PID 1`, usually **systemd**), which mounts disks and starts services.
   - 內核啟動第一個行程（PID 1，通常是 systemd），掛載硬碟並啟動服務。

---

## III. Quantitative Analysis Table (量化指標分析)

| Phase (階段) | Est. Latency (預估耗時) | CPU Mode (CPU 模式) | Resource Usage (資源消耗) |
|---|---|---|---|
| **Power On / RESET** | < 1 ms | 16-bit Real Mode | Fixed ROM Address. |
| **POST (Firmware)** | ~1s - 10s | 16-bit / 32-bit | Full hardware probe. |
| **Bootloader (GRUB)** | ~1s - 2s | Transition to 32/64 | Minimal RAM usage. |
| **Kernel Loading** | ~1s - 3s | 64-bit Protected Mode | Memory Mapping (MMU On). |
| **User Space (init)** | ~5s - 30s | 64-bit | Peak Disk/CPU (Service startup). |

---

## IV. Ecosystem Comparison (生態系橫向對比)

| Feature (特性) | Legacy BIOS | modern UEFI | Note (備註) |
|---|---|---|---|
| **Drive Support** | MBR (< 2TB) | GPT (> 2TB) | UEFI 支援更大的硬碟分割。 |
| **Code Execution** | Assembly (16-bit) | C (32/64-bit) | UEFI 更易維護與擴充。 |
| **Security** | None | **Secure Boot** | UEFI 可驗證簽章防止惡意代碼。 |
| **Interface** | Text-only | GUI / Mouse supported | UEFI 提供更友善的設定介面。 |

---

## V. Troubleshooting: Common Hang Points (常見錯誤與停滯點)

| Hang Point (停滯位置) | Error Symptom (錯誤徵狀) | Probable Cause (可能原因) |
|---|---|---|
| **POST Stage** | Black screen, beep codes. | Hardware failure (RAM/GPU unseated). (硬體故障，如記憶體沒插好。) |
| **Boot Selection** | "No bootable device found." | Defective HDD, wrong boot order, or wiped MBR. (硬碟損壞或啟動順序錯誤。) |
| **Bootloader** | `grub rescue>` prompt. | GRUB config missing or partition ID changed. (GRUB 配置損失或分割區 ID 變動。) |
| **Kernel Loading** | **Kernel Panic** / Blue Screen. | Incompatible drivers or corrupted kernel image. (驅動不相容或內核毀損。) |
| **Systemd / Init** | Stuck at a specific service. | Network timeout or disk mount failure (fstab error). (網路超時或掛載失敗。) |

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Dead Batteries (CMOS)**: If the CMOS battery dies, BIOS settings revert to default, causing boot order resets. (CMOS 電池沒電會導致 BIOS 設定重置，影響啟動順序。)
2. **Overclocking Failure**: A failed CPU/RAM overclock can cause the system to hang during POST or produce intermittent Kernel Panics. (超頻失敗會導致 POST 停滯或不穩定的內核崩潰。)
3. **Initramfs Missing**: If the kernel cannot find the initial RAM disk, it cannot mount the root filesystem, leading to a "Boot loop". (找不到 initramfs 會導致無法掛載根目錄，造成啟動迴圈。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Real Mode | 實模式 | Ancient x86 mode with 1MB addressable memory. (傳統 x86 模式，僅能存取 1MB 記憶體。) |
| Protected Mode | 保護模式 | Modern x86 mode supporting virtual memory and paging. (支援虛擬記憶體與分頁的現代模式。) |
| Initramfs | 臨時根檔案系統 | Initial RAM-based filesystem extracted by kernel. (內核解壓的初步記憶體檔案系統。) |
| Reset Vector | 重置向量 | The location where the CPU starts execution after reset. (CPU 重設後開始執行的位置。) |
| Systemd | 系統守護行程 | The modern init system for Linux. (Linux 的現代初始化系統。) |
