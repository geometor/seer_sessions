┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1745 │       410 │      0 │  2155 │   6.5493 │
│ 002-response.json │   2241 │       485 │      0 │  2726 │   9.1040 │
│ 003-response.json │   3468 │       826 │      0 │  4294 │  10.2393 │
│ 004-response.json │   4378 │       358 │      0 │  4736 │   4.5440 │
│ 005-response.json │   5502 │       692 │      0 │  6194 │   7.6090 │
│ 006-response.json │   6278 │       358 │      0 │  6636 │   5.1449 │
│ TOTAL             │  23612 │      3129 │      0 │ 26741 │  43.1905 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                                        Code File: 002                                        
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status                              ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ FAILED                              │ ✅   │ ✅      │ ❌          │ 2           │
│ 2       │ ERROR: cannot unpack non-iterable   │ N/A  │ N/A     │ N/A         │ N/A         │
│         │ NoneType object                     │      │         │             │             │
│ 3       │ ERROR: cannot unpack non-iterable   │ N/A  │ N/A     │ N/A         │ N/A         │
│         │ NoneType object                     │      │         │             │             │
└─────────┴─────────────────────────────────────┴──────┴─────────┴─────────────┴─────────────┘
                                        Code File: 003                                        
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status                              ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (5,3) (4,4)                         │      │         │             │             │
│ 2       │ PASSED                              │ ✅   │ ✅      │ ✅          │ 0           │
│ 3       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (5,3) (3,5)                         │      │         │             │             │
└─────────┴─────────────────────────────────────┴──────┴─────────┴─────────────┴─────────────┘
                                        Code File: 004                                        
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status                              ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (10,12) (4,4)                       │      │         │             │             │
│ 2       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (11,12) (5,3)                       │      │         │             │             │
│ 3       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (12,12) (3,5)                       │      │         │             │             │
└─────────┴─────────────────────────────────────┴──────┴─────────┴─────────────┴─────────────┘
                                        Code File: 005                                        
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status                              ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (3,5) (4,4)                         │      │         │             │             │
│ 2       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (3,5) (5,3)                         │      │         │             │             │
│ 3       │ PASSED                              │ ✅   │ ✅      │ ✅          │ 0           │
└─────────┴─────────────────────────────────────┴──────┴─────────┴─────────────┴─────────────┘
                                        Code File: 006                                        
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status                              ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (10,12) (4,4)                       │      │         │             │             │
│ 2       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (11,12) (5,3)                       │      │         │             │             │
│ 3       │ ERROR: operands could not be        │ ❌   │ ✅      │ ❌          │ N/A         │
│         │ broadcast together with shapes      │      │         │             │             │
│         │ (12,12) (3,5)                       │      │         │             │             │
└─────────┴─────────────────────────────────────┴──────┴─────────┴─────────────┴─────────────┘
