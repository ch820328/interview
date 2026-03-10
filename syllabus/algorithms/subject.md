# Algorithm Syllabus — Topic Index (演算法題庫索引)

> 命名規則：新題目存到對應分類資料夾，檔名用 `{topic_keyword}.md`

---

| # | Category (分類) | Folder | 代表題型 |
|---|---|---|---|
| 1 | **Array & Hashing** | `01_array_hashing/` | Prefix Sum, HashMap 查找 |
| 2 | **Two Pointers** | `02_two_pointers/` | 區間合併、雙指針碰撞 |
| 3 | **Sliding Window** | `03_sliding_window/` | 固定/可變視窗最大值 |
| 4 | **Stack & Queue** | `04_stack_queue/` | 單調堆疊、括號匹配 |
| 5 | **Binary Search** | `05_binary_search/` | 搜尋答案空間 |
| 6 | **Linked List** | `06_linked_list/` | LRU Cache、快慢指針 |
| 7 | **Trees** | `07_trees/` | BST、DFS/BFS 遍歷 |
| 8 | **Heap / Priority Queue** | `08_heap/` | Top-K、Meeting Rooms |
| 9 | **Backtracking** | `09_backtracking/` | 排列組合、N-Queens |
| 10 | **Graphs** | `10_graphs/` | BFS/DFS、拓撲排序、最短路徑 |
| 11 | **Dynamic Programming** | `11_dynamic_programming/` | Word Break、背包問題 |
| 12 | **Advanced DS** | `12_advanced/` | Trie、Segment Tree、設計題 |

---

## 已練習題目

### 01 Array & Hashing
| 檔案 | 題目摘要 |
|------|---------|
| [array_and_string.md](01_array_hashing/array_and_string.md) | 陣列與字串基礎 |
| [hash_table.md](01_array_hashing/hash_table.md) | HashMap 查找 |
| [prefix_sum.md](01_array_hashing/prefix_sum.md) | 前綴和 |

### 02 Two Pointers
| 檔案 | 題目摘要 |
|------|---------|
| [two_pointers.md](02_two_pointers/two_pointers.md) | 雙指針基礎 |
| [merge_intervals.md](02_two_pointers/merge_intervals.md) | 區間合併 |

### 03 Sliding Window
| 檔案 | 題目摘要 |
|------|---------|
| [sliding_window.md](03_sliding_window/sliding_window.md) | 滑動視窗基礎 |
| [sliding_window_min_of_max.md](03_sliding_window/sliding_window_min_of_max.md) | 所有長度 k 子陣列最大值的最小值（單調隊列）✅ 新 |

### 04 Stack & Queue
| 檔案 | 題目摘要 |
|------|---------|
| [stack_and_queue.md](04_stack_queue/stack_and_queue.md) | 堆疊與佇列基礎 |
| [monotonic_stack_daily_temperatures.md](04_stack_queue/monotonic_stack_daily_temperatures.md) | Daily Temperatures（單調堆疊）|
| [decode_string.md](04_stack_queue/decode_string.md) | 解碼字串 |

### 05 Binary Search
| 檔案 | 題目摘要 |
|------|---------|
| [binary_search.md](05_binary_search/binary_search.md) | 二分搜尋基礎 |
| [binary_search_koko.md](05_binary_search/binary_search_koko.md) | Koko Eating Bananas |
| [binary_search_on_answer_koko.md](05_binary_search/binary_search_on_answer_koko.md) | 答案空間二分搜尋 |

### 04 Prefix Sum / 前綴和
| 檔案 | 題目摘要 |
|------|---------|
| [range_sum_query_immutable.md](04_prefix_sum/range_sum_query_immutable.md) | 區域和檢索（靜態陣列） |
| [random_pick_with_weight.md](04_prefix_sum/random_pick_with_weight.md) | 按權重隨機選擇 |
| [random_point_in_rectangles.md](04_prefix_sum/random_point_in_rectangles.md) | 矩陣隨機取點（前綴和 + 二分搜尋）✅ 新 |

### 06 Linked List
| 檔案 | 題目摘要 |
|------|---------|
| [linked_list.md](06_linked_list/linked_list.md) | 鏈結串列基礎 |
| [lru_cache.md](06_linked_list/lru_cache.md) | LRU Cache |

### 07 Trees
| 檔案 | 題目摘要 |
|------|---------|
| [binary_tree_and_bst.md](07_trees/binary_tree_and_bst.md) | 二元樹與 BST |

### 08 Heap / Priority Queue
| 檔案 | 題目摘要 |
|------|---------|
| [heap_and_priority_queue.md](08_heap/heap_and_priority_queue.md) | 堆積基礎 |
| [heap_meeting_rooms.md](08_heap/heap_meeting_rooms.md) | Meeting Rooms II |

### 09 Backtracking
| 檔案 | 題目摘要 |
|------|---------|
| [backtracking.md](09_backtracking/backtracking.md) | 回溯基礎 |

### 10 Graphs
| 檔案 | 題目摘要 |
|------|---------|
| [graph_theory_and_traversal.md](10_graphs/graph_theory_and_traversal.md) | 圖論與遍歷基礎 |
| [graph_course_schedule.md](10_graphs/graph_course_schedule.md) | Course Schedule（拓撲排序）|
| [advanced_graph_shortest_path.md](10_graphs/advanced_graph_shortest_path.md) | 最短路徑進階 |
| [topological_sort.md](10_graphs/topological_sort.md) | 拓撲排序 |
| [union_find.md](10_graphs/union_find.md) | Union Find（並查集）|
| [robot_room_cleaner.md](10_graphs/robot_room_cleaner.md) | 掃地機器人（DFS 物理回溯） |
| [maze_with_keys.md](10_graphs/maze_with_keys.md) | 迷宮與鑰匙（Greedy BFS 可達性優化）✅ 新 |


### 11 Dynamic Programming
| 檔案 | 題目摘要 |
|------|---------|
| [dynamic_programming.md](11_dynamic_programming/dynamic_programming.md) | DP 基礎 |
| [dp_word_break.md](11_dynamic_programming/dp_word_break.md) | Word Break |

### 15 Heuristics / 啟發式搜索
| 檔案 | 題目摘要 |
|------|---------|
| [word_guessing_strategy.md](15_heuristics/word_guessing_strategy.md) | Wordle 猜字策略（一致性過濾 + 頻率啟發式）✅ 新 |

### 12 Advanced Data Structures
| 檔案 | 題目摘要 |
|------|---------|
| [trie.md](12_advanced/trie.md) | 字典樹 Trie |
| [segment_tree_and_fenwick.md](12_advanced/segment_tree_and_fenwick.md) | 線段樹 + 樹狀陣列 |
| [insert_delete_getrandom.md](12_advanced/insert_delete_getrandom.md) | Insert Delete GetRandom O(1) |
| [stock_price_class.md](12_advanced_ds/stock_price_class.md) | 股票價格波動（HashMap + Heap 延遲刪除）✅ 新 |
