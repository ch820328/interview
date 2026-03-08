# Syllabus: Decode String (String Parsing with Stack)

## 1. Problem Statement & Constraints / 題目描述與約束
**English:**  
Given an encoded string, return its decoded string. The encoding rule is: `k[encoded_string]`, where the `encoded_string` inside the square brackets is being repeated exactly `k` times. `k` is a positive integer. Assume the input is always valid.

**Chinese (Traditional):**  
給定一個加密字串，返回其解碼後的字串。加密規則為：`k[encoded_string]`，其中方括號內的 `encoded_string` 正好重複 `k` 次。`k` 為正整數。假設輸入始終有效。

**Constraints:**
- $1 \le s.length \le 30$
- $s$ consists of lowercase English letters, digits, and square brackets.
- $k$ is in the range $[1, 300]$.

## 2. Clarification Q&A / 澄清與問答
| Question (EN) | Answer (EN) | Question (ZH) | Answer (ZH) |
|---|---|---|---|
| Can brackets be nested? | Yes, e.g., `3[a2[c]]`. | 括號可以嵌套嗎？ | 可以，例如 `3[a2[c]]`。 |
| Are there multi-digit numbers? | Yes, e.g., `10[a]`. | 會有超過一位數的數字嗎？ | 會，例如 `10[a]`。 |
| How to handle chars outside `[]`? | Included as-is, e.g., `abc2[d]`. | 如何處理括號外的字元？ | 直接包含，例如 `abc2[d]`。 |

## 3. Brute Force vs Optimal / 暴力法 vs 最優解
| Method | Time Complexity | Space Complexity | Notes |
|---|---|---|---|
| **Brute Force (Recursion)** | $O(L)$ | $O(N)$ | Simple but can hit recursion depth limits. |
| **Optimal (Stack)** | $O(L)$ | $O(N + D)$ | Iterative, efficient, and avoids recursion overhead. |

## 4. Final Solution (Python) / 最終代碼
```python
class Solution:
    def decodeString(self, s: str) -> str:
        stack = []  # Stores (prev_string, repeat_count)
        curr_str = ""
        curr_num = 0
        
        for char in s:
            if char.isdigit():
                curr_num = curr_num * 10 + int(char)
            elif char == '[':
                # Push state and reset for new scope
                stack.append((curr_str, curr_num))
                curr_str = ""
                curr_num = 0
            elif char == ']':
                # Pop state and merge
                prev_str, count = stack.pop()
                curr_str = prev_str + (curr_str * count)
            else:
                curr_str += char
        return curr_str
```

## 5. Dry Run Table / 逐步執行追蹤
**Input:** `3[a2[c]]`
| Step | Char | `curr_num` | `curr_str` | `stack` |
|---|---|---|---|---|
| 1 | `3` | 3 | "" | `[]` |
| 2 | `[` | 0 | "" | `[("", 3)]` |
| 3 | `a` | 0 | "a" | `[("", 3)]` |
| 4 | `2` | 2 | "a" | `[("", 3)]` |
| 5 | `[` | 0 | "" | `[("", 3), ("a", 2)]` |
| 6 | `c` | 0 | "c" | `[("", 3), ("a", 2)]` |
| 7 | `]` | 0 | "acc" | `[("", 3)]` |
| 8 | `]` | 0 | "accaccacc" | `[]` |

## 6. Common Bugs / 常見錯誤
| Bug | Prevention |
|---|---|
| Forgetting multi-digit numbers. | Always use `res = res * 10 + digit`. |
| Not clearing `curr_num` after `[`. | Ensure `curr_num = 0` immediately after pushing to stack. |
| Mismanaging characters before `[`. | Push `curr_str` to stack to save the prefix. |

## 7. Full Evaluation / 完整評估 (Bilingual)
**Rating: Hire / 錄取評等：錄取**

**Strengths:**
- User correctly identified the Stack approach for nested structures. (面試者正確識別了使用堆疊處理嵌套結構的方法。)
- Handled multi-digit logic and prefix strings correctly. (正確處理了多位數邏輯和前綴字串。)

**Gaps to L5:**
- Initially missed the distinction between $O(N)$ and $O(L)$ (output length). (最初未能區分輸入長度 $O(N)$ 和輸出長度 $O(L)$ 之間的差異。)

## 8. Actionable Corrections / 改進建議 (Bilingual)
1. **Verbalize Complexity**: Practice explaining why string concatenation is $O(K)$ and how that affects the total complexity. (練習解釋為什麼字串連接是 $O(K)$，以及這如何影響總體複雜度。)
2. **Handle Large Output**: Think about what happens if the result exceeds memory (e.g., extremely large `k`). (思考如果結果超出記憶體限制會發生什麼，例如極大的 `k` 值。)
