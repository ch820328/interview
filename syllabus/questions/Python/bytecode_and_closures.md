# Python Bytecode & Closures: Expert Analysis (Python 位元組碼與閉包：專家級分析)

## I. Problem Statement & Nuances (題目與細節)
How does Python implement "Closures"? Why can an inner function still access variables from an outer function even after the outer function has finished execution?
Python 如何實現「閉包」？為什麼內部函式在外部函式執行完畢後，仍能存取外部函式的變數？

**Nucleus Insights (核心觀點):**
- **Cell Objects**: Closures are implemented using `cell` objects that act as a shared container between scopes. (閉包透過「單元對象 (Cell Objects)」實現，作為不同作用域間的共享容器。)
- **`co_freevars` & `co_cellvars`**: The compiler identifies variables that are part of a closure during compile time and marks them for special handling. (編譯期間識別閉包變數並標記。)
- **Bytecode Dispatch**: Accessing a closure variable uses `LOAD_DEREF` instead of the faster `LOAD_FAST`. (存取閉包變數使用 `LOAD_DEREF` 指令，而非更快的 `LOAD_FAST`。)

---

## II. Mechanical Deep-Dive: Cell Objects (底層原理：單元對象)

When a variable is used in an inner function, Python doesn't just copy the value. It wraps the variable in a **PyCellObject**.
當變數在內部函式中使用時，Python 將其封裝在一個專有的 Cell 對象中。

1. **Outer Scope**: Creates the cell and stores the reference.
2. **Inner Function**: The function object's `__closure__` attribute holds a tuple of these cells.
3. **Execution**: When needed, the code "dereferences" the cell to get the actual value.

---

## III. Quantitative Analysis: Scope Performance (量化指標)

| Instruction | Target (目標) | Cost (耗時比) | Reason (原因) |
|---|---|---|---|
| **LOAD_FAST** | Local variables. | $1.0\times$ | Direct array indexing in the stack frame. |
| **LOAD_DEREF** | Closure variables. | $1.3\times - 1.5\times$ | Requires following a pointer to the cell. |
| **LOAD_GLOBAL** | Global/Built-in. | $2.0\times - 3.0\times$ | Requires HashMap lookup in globals/builtins. |

---

## IV. Bytecode Analysis (位元組碼追蹤)

Consider this code:
```python
def outer(x):
    def inner():
        return x
    return inner
```

### Bytecode for `inner` (using `dis.dis`):
```text
  3           0 LOAD_DEREF               0 (x)
              2 RETURN_VALUE
```
*Note: `LOAD_DEREF` is the smoking gun of a closure.*

### Analyzing `outer`:
```text
  2           0 LOAD_CLOSURE             0 (x)
              2 BUILD_TUPLE              1
              4 LOAD_CONST               1 (<code object inner at ...>)
              6 LOAD_CONST               2 ('outer.<locals>.inner')
              8 MAKE_FUNCTION            8 (closure)
             10 RETURN_VALUE
```
*Note: `MAKE_FUNCTION` with flag `8` indicates it is creating a closure function.*

---

## V. Interviewer Traps: Delayed Binding (面試官陷阱)

**Q:** 下方代碼的輸出是什麼？為什麼？
```python
funcs = []
for i in range(3):
    funcs.append(lambda: i)

print([f() for f in funcs])
```
**A (專家級回答)**: 輸出為 `[2, 2, 2]`。
**原因**: 閉包綁定的是 **變數本身 (Cell)** 而非當下的值。當 `i` 增加到 2 時，所有閉包都指向同一個 `i` 的 Cell。這被稱為 **Late Binding (延遲綁定)**。
**解法**: 使用預設參數 `lambda i=i: i` 或 `functools.partial` 來強迫立即綁定。

---

## VI. Technical Term Dictionary (技術術語字典)

| Term (術語) | Translation (中文翻譯) | Description (說明) |
|---|---|---|
| Free Variable | 自由變數 | A variable used in a function that is not defined in that function. (在函式中使用但未在其中定義的變數。) |
| Cell Object | 單元對象 | An internal CPython object used to implement closures. (實現閉包的內部 CPython 對象。) |
| DEREF | 解引用 | The process of getting the value stored in a cell. (從 Cell 中獲取儲存的值的過程。) |
| Function Object | 函式對象 | The runtime instance of a function, containing `__closure__`, `__code__`, etc. (包含閉包與代碼對象的函式執行實體。) |
