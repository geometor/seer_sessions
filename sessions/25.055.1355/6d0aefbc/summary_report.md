┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1771 │       443 │      0 │  2214 │   7.5929 │
│ 002-response.json │   2076 │       280 │      0 │  2356 │   3.8712 │
│ 003-response.json │   1534 │       972 │      0 │  2506 │  11.6197 │
│ 004-response.json │   2302 │       333 │      0 │  2635 │   3.9347 │
│ 005-response.json │   1588 │      4924 │      0 │  6512 │  36.7063 │
│ 006-response.json │   6313 │       274 │      0 │  6587 │   2.9699 │
│ 007-response.json │   1771 │       492 │      0 │  2263 │   6.9968 │
│ 008-response.json │   2125 │       192 │      0 │  2317 │   2.8265 │
│ TOTAL             │  19480 │      7910 │      0 │ 27390 │  76.5180 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 8           │ 55.56 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 11          │ 38.89 │
│ 3       │ ❌    │ ✅   │ ✅      │ ✅          │ 7           │ 61.11 │
│ 4       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 88.89 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 004-py_02-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 8           │ 55.56 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 11          │ 38.89 │
│ 3       │ ❌    │ ✅   │ ✅      │ ✅          │ 7           │ 61.11 │
│ 4       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 88.89 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 005-py_03-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 8           │ 55.56 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 11          │ 38.89 │
│ 3       │ ❌    │ ✅   │ ✅      │ ✅          │ 7           │ 61.11 │
│ 4       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 88.89 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 006-py_04-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 8           │ 55.56 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 11          │ 38.89 │
│ 3       │ ❌    │ ✅   │ ✅      │ ✅          │ 7           │ 61.11 │
│ 4       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 88.89 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                        Code File: 008-py_05-test                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 008-py_05-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 4       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
