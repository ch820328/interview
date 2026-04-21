# Golang Interface: Runtime Internals (Go 介面：底層運行機制)

## I. The Core Structs: `eface` vs `iface` (核心結構)
Go 的介面在運行時並非單一結構，而是根據是否包含方法分為兩種。

### 1. `eface` (Empty Interface / 空介面)
對應 `interface{}`。由於不含方法，它只需要紀錄型別與數據。
```go
// src/runtime/runtime2.go
type eface struct {
    _type *_type // 指向型別元數據 (Type Metadata)
    data  unsafe.Pointer // 指向實際數據的指標 (Value pointers)
}
```

### 2. `iface` (Non-empty Interface / 帶方法介面)
對應 `type Reader interface { Read() }`。它包含一個額外的 `itab` (Interface Table)。
```go
type iface struct {
    tab  *itab
    data unsafe.Pointer
}

type itab struct {
    inter *interfacetype // 介面的型別定義
    _type *_type          // 具體實作的「動態型別」元數據
    hash  uint32         // 用於型別斷言 (Type Assertion) 的快速匹配
    _     [4]byte
    fun   [1]uintptr     // 硬核點：指向具體方法實作的函式指標陣列
}
```

---

## II. The "itab" Caching Mechanism (itab 緩存機制)
**面試精選：** *「每次 interface 轉換都要重新計算 itab 嗎？」*
1. **動態綁定**：介面轉換是發生在 Runtime 的。
2. **全局 Cache**：Runtime 維護一個 Hash Map，以 `(interface type, implementation type)` 為 Key。
3. **性能優化**：第一次轉換時有查表開銷（包含方法查驗），隨後觸發 Cache 命中，性能接近直接呼叫。

---

## III. Type Assertion: Under the Hood (型別斷言底層)
當您執行 `v, ok := i.(MyStruct)` 時，Runtime 做了什麼？
1. **檢查 `_type` 雜湊值**：比較介面中的 `tab._type` (或 `eface._type`) 與 `MyStruct` 的型別資料。
2. **記憶體轉換**：若匹配，將數據指標 `iface.data` 轉成 `MyStruct` 返回。
3. **效率**：這是核心路徑，經過高度彙編優化。

---

## IV. Quantitative Analysis: Interface Overhead (接口開銷量化)

| Operation | Relative Cost | Reason (原因) |
|---|---|---|
| **Direct Call** | $1\times$ | CPU 直接跳轉指令。 |
| **Interface Call** | $1.2\times - 1.5\times$ | 多一層指標跳轉 (`iface -> itab -> fun`)。 |
| **Type Assertion** | $2\times - 5\times$ | 需要雜湊值比對與類型檢查。 |

---

## V. Interviewer Traps: Crucial Nuances (面試官陷阱)

### Trap 1: "nil interface" 與 "interface with nil value"
**Q:** 為什麼下方程式碼會印出 `false`？
```go
var a *MyStruct = nil
var i interface{} = a
fmt.Println(i == nil) // 返回 false
```
**A (專家級回答)**：因為 `i` (eface) 的 `_type` 欄位已經填入了 `*MyStruct` 的資訊（型別元數據），不再是真正的零值。只有當 `eface._type` 且 `eface.data` 皆為 `nil` 時，`i == nil` 才會成立。

### Trap 2: 通過指針還是值實現介面？
**Q:** 為什麼變數接收者 (Value Receiver) 能滿足指標介面，反之則不行？
**A**: 因為 Go 可以自動將值取地址 (`&v`) 以滿足指標需求，但無法保證指標背後的數據是可定址的 (Addressable)，且指標接收者暗示了「狀態修改」，值傳遞會失去此意義。

---

## VI. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Dynamic Dispatch | 動態派發 | 根據運行時的實際型別決定呼叫哪個方法的過程。 |
| Pointer Indirection | 指標跳轉 | 透過指標尋找數據的過程，是介面效能損失的主因。 |
| Concrete Type | 具體型別 | 被轉換進介面的原始型別（如 `int`, `MyStruct`）。 |
| itab | 介面表 | 存儲介面型別與實作型別對應關係的結構。 |
