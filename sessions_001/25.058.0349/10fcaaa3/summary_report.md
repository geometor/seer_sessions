╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                       Task Summary                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1797 │       623 │      0 │  2420 │   9.2010 │
│ 002-response.json │   2283 │       386 │      0 │  2669 │   4.6476 │
│ 003-response.json │   1637 │      1582 │      0 │  3219 │  17.2407 │
│ 004-response.json │   3013 │       403 │      0 │  3416 │   4.5353 │
│ 005-response.json │   1654 │      8192 │      0 │  9846 │  66.9569 │
│ 006-response.json │   9646 │       445 │      0 │ 10091 │   4.6243 │
│ TOTAL             │  20030 │     11631 │      0 │ 31661 │ 107.2060 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 6           │ 81.25 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 30          │ 37.50 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 33          │ 45.00 │
│ 4       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 93.75 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 004-py_02-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 8           │ 75.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 30          │ 37.50 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 33          │ 45.00 │
│ 4       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 93.75 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                     Code File: 005-py_03-test                      
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───┘
                     Code File: 005-py_03-train                     
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───┘
                       Code File: 006-py_04-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 8           │ 75.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 30          │ 37.50 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 33          │ 45.00 │
│ 4       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 93.75 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
