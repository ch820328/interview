# UEFI Boot Phases: PI Architecture Deep-Dive (UEFI 啟動階段：PI 架構深度解析)

## I. Problem Statement & Nuances (題目與細節)
Explain the specific stages of a UEFI boot process according to the Platform Initialization (PI) specification. What happens in SEC, PEI, and DXE?
請解釋根據 PI 規範，UEFI 啟動過程的具體階段。在 SEC、PEI 與 DXE 中分別發生了什麼？

**Nucleus Insights (核心觀點):**
- **Hand-off via HOBs (Hand-Off Blocks)**: How information (like memory map) is passed from the memory-constrained PEI phase to the driver-rich DXE phase. (資訊如何從受限的 PEI 階段傳遞到 DXE 階段。)
- **CAR (Cache-As-RAM)**: Before physical RAM is initialized, the CPU uses its cache as temporary memory. (在實體記憶體初始化前，CPU 將快取作為暫時記憶體使用。)
- **Dispatcher Logic**: DXE drivers are not loaded in a fixed order; they are dispatched based on dependencies. (DXE 驅動程式並非固定順序加載，而是基於依賴關係進行調度。)

---

## II. The 6 Phases of UEFI (UEFI 的六大階段)

| Phase (階段) | Name (名稱) | Key Responsibility (關鍵任務) |
|---|---|---|
| **SEC** | Security | Handles **Reset Vector**, sets up **CAR**, transitions from Real Mode. (處理重置向量，建立 CAR，從實模式切換。) |
| **PEI** | Pre-EFI Init | **Memory Discovery**, initializes chipset/CPU fundamentals. (記憶體偵測，初始化晶片組與 CPU 基礎。) |
| **DXE** | Driver Execution | Loads **UEFI Drivers** (PCI, Flash, USB) via a Dispatcher. (透過調度器加載主系統驅動程式。) |
| **BDS** | Boot Device Selection | Handles the **Boot Manager UI**, picks the boot device. (處理啟動管理介面，挑選啟動裝置。) |
| **TSL** | Transient System Loader| OS Loader executes; transition from EFI to OS kernel. (啟動程式執行；從 EFI 交接至 OS 內核。) |
| **RT** | Run Time | Services that remain in memory (e.g., SetVariable). (留在記憶體中的服務，如設置變數。) |

---

## III. Mechanical Deep-Dive: From PEI to DXE (底層原理：從 PEI 到 DXE)

### 1. The PEI Stage (Pre-EFI Initialization)
The main goal of PEI is to **initialize memory**. Since there is no RAM yet, it runs in **CAR** mode. It identifies the hardware and creates **HOBs** (Hand-Off Blocks).
PEI 的主要目標是**初始化記憶體**。由於此時還沒有 RAM，它運行在 **CAR** 模式。它會辨識硬體並建立 **HOBs**。

### 2. The DXE Stage (Driver Execution Environment)
Once RAM is available, the **DXE Foundation** is loaded. It starts a **Dispatcher** that reads all the DXE drivers (FEIs) and executes them if their dependencies are met.
一旦記憶體可用，**DXE 基金會** 就會被加載。它會啟動一個**調度器**，讀取所有 DXE 驅動，並在滿足依賴條件時執行它們。

---

## IV. Quantitative Analysis Table (量化數據分析)

| Metric (指標) | PEI Phase | DXE Phase |
|---|---|---|
| **Memory Available** | CPU Cache (Typically < 1 MB) | Full System RAM (GBs) |
| **Code Type** | PIC (Position Independent Code) | PE/COFF Executables |
| **Driver Count** | Minimal (Essential Silicon init) | Hundreds (Full peripheral support) |
| **Communication** | PPIs (PEIM-to-PEIM Interface) | Protocols (Handle-based) |

---

## V. Troubleshooting: Hang Points in UEFI (UEFI 常見停滯點)

| Hang Point (停滯位置) | Error Symptom (錯誤徵狀) | Probable Cause (可能原因) |
|---|---|---|
| **SEC Phase** | Immediate restart / No power. | Corrupted SPI Flash / CPU microcode error. (BIOS 晶片損毀或微代碼錯誤。) |
| **PEI Phase** | Stuck at a specific POST code (e.g., 55). | **RAM Training Failure** or CPU socket issue. (記憶體訓練失敗或 CPU 插槽問題。) |
| **DXE Phase** | Stuck at logo / UI splash. | NVMe/Storage driver timeout or PCI resource conflict. (儲存設備驅動超時或 PCI 資源衝突。) |
| **BDS Phase** | "Entering Setup..." but hangs. | USB peripheral interference / Stuck key. (USB 周邊干擾或按鍵卡住。) |

---

## VI. Failure Modes & Edge Cases (失敗模式與邊界)

1. **Memory Training**: During PEI, the BIOS must calibrate each RAM stick for timing/voltage. This can take seconds and is a frequent point of failure in high-speed DDR kits. (在 PEI 期間，BIOS 必須校準記憶體參數，這是常見的高頻記憶體失效點。)
2. **NVRAM Corruption**: DXE stores variables in the Flash (NVRAM). If this gets corrupted (e.g., by a bad OS update), the DXE dispatcher might hang. (DXE 將變數存在快閃記憶體中。若毀損，調度器可能會停滯。)

---

## VII. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| CAR | 快取作為記憶體 | Using CPU cache as temporary stack before RAM is up. (在 RAM 啟動前將 CPU 快取作為暫時堆疊。) |
| HOB | 交接塊 | Data structures used to pass info between PEI and DXE. (用於在 PEI 與 DXE 之間傳遞資訊的數據結構。) |
| PPI | PEI 間介面 | Method for PEIMs to communicate with each other. (PEI 模組間互相溝通的方法。) |
| Protocol | 協定 | A software interface produced and consumed in DXE. (在 DXE 中產生與使用的軟體介面。) |
