╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                       Task Summary                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1753 │       338 │      0 │  2091 │   5.6441 │
│ 002-response.json │   1952 │       239 │      0 │  2191 │  27.3495 │
│ 003-response.json │   1490 │      1090 │      0 │  2580 │  12.3663 │
│ 004-response.json │   2376 │       265 │      0 │  2641 │   3.2106 │
│ 005-response.json │   1516 │       960 │      0 │  2476 │  12.4539 │
│ 006-response.json │   2275 │       418 │      0 │  2693 │   3.8331 │
│ 007-response.json │   1765 │       529 │      0 │  2294 │   7.6391 │
│ 008-response.json │   2155 │       225 │      0 │  2380 │  17.5598 │
│ TOTAL             │  15282 │      4064 │      0 │ 19346 │  90.0565 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 1           │ 91.67  │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 5           │ 75.00  │
│ 4       │ ❌    │ ✅   │ ✅      │ ❌          │ 11          │ 63.33  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 004-py_02-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 83.33  │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 6           │ 70.00  │
│ 4       │ ❌    │ ✅   │ ✅      │ ❌          │ 12          │ 60.00  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 006-py_03-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 8           │ 11.11 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 10          │ 16.67 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 14          │ 30.00 │
│ 4       │ ❌    │ ✅   │ ✅      │ ❌          │ 18          │ 40.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                        Code File: 008-py_04-test                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 008-py_04-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 4       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
