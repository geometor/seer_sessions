┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1739 │       431 │      0 │  2170 │  81.4741 │
│ 002-response.json │   2031 │       209 │      0 │  2240 │   3.3369 │
│ 003-response.json │   1461 │      2234 │      0 │  3695 │  21.2595 │
│ 004-response.json │   2685 │      2022 │      0 │  4707 │  20.9475 │
│ 005-response.json │   4503 │       279 │      0 │  4782 │   3.8489 │
│ 006-response.json │   3491 │       169 │      0 │  3660 │   2.7956 │
│ 007-response.json │   1741 │       408 │      0 │  2149 │   6.5293 │
│ 008-response.json │   2010 │       146 │      0 │  2156 │   3.4959 │
│ 009-response.json │   1397 │       893 │      0 │  2290 │  11.3359 │
│ 010-response.json │   2083 │       289 │      0 │  2372 │   3.6282 │
│ TOTAL             │  23141 │      7080 │      0 │ 30221 │ 158.6518 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 4       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                                  Code File: 003-py_02-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                                  Code File: 004-py_03-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                      Code File: 005-py_04-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ N/A   │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 3       │ N/A   │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 4       │ N/A   │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                      Code File: 006-py_05-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ❌      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ✅   │ ❌      │ ❌          │ 1           │ 0.00 │
│ 4       │ ❌    │ ❌   │ ❌      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 008-py_06-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 4       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                        Code File: 010-py_07-test                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 010-py_07-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 4       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
