┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   5317 │       522 │      0 │  5839 │   9.5823 │
│ 002-response.json │   5698 │       814 │      0 │  6512 │   9.5800 │
│ 003-response.json │  16711 │      1918 │      0 │ 18629 │  22.7268 │
│ 004-response.json │   1709 │       553 │      0 │  2262 │   8.1975 │
│ 005-response.json │   2057 │        87 │      0 │  2144 │   1.9026 │
│ 006-response.json │  18424 │      1206 │      0 │ 19630 │  13.0370 │
│ 007-response.json │   5317 │       721 │      0 │  6038 │  10.5352 │
│ 008-response.json │   5899 │       884 │      0 │  6783 │   9.5707 │
│ TOTAL             │  61132 │      6705 │      0 │ 67837 │  85.1322 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 161         │ 82.11 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 216         │ 76.00 │
│ 3       │ N/A   │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                                  Code File: 003-py_02-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                       Code File: 005-py_03-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 76          │ 91.56 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 84          │ 90.67 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 79          │ 91.22 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 006-py_04-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 372         │ 58.67 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 247         │ 72.56 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 362         │ 59.78 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 008-py_05-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 76          │ 91.56 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 84          │ 90.67 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 79          │ 91.22 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
