┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1937 │       558 │      0 │  2495 │   8.8870 │
│ 002-response.json │   2355 │       585 │      0 │  2940 │   6.6055 │
│ 003-response.json │   2671 │       957 │      0 │  3628 │  14.0338 │
│ 004-response.json │   3427 │       801 │      0 │  4228 │   7.9285 │
│ 005-response.json │   1937 │       620 │      0 │  2557 │  16.7716 │
│ 006-response.json │   2419 │       656 │      0 │  3075 │   5.8763 │
│ TOTAL             │  14746 │      4177 │      0 │ 18923 │  60.1028 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 9           │ 83.64  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 004-py_02-test                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 9           │ 83.64 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 004-py_02-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 006-py_03-test                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 9           │ 83.64 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 006-py_03-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
