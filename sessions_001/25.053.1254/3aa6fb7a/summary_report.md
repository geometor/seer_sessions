┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1911 │       463 │      0 │  2374 │   7.0305 │
│ 002-response.json │   2236 │       738 │      0 │  2974 │   7.4233 │
│ 003-response.json │   2753 │      2323 │      0 │  5076 │  21.3670 │
│ 004-response.json │   2564 │      1112 │      0 │  3676 │  13.6821 │
│ 005-response.json │   3471 │       550 │      0 │  4021 │   5.4844 │
│ 006-response.json │   2565 │       953 │      0 │  3518 │  12.0780 │
│ 007-response.json │   3314 │       570 │      0 │  3884 │   4.8631 │
│ 008-response.json │   4871 │       742 │      0 │  5613 │   6.7283 │
│ 009-response.json │   1911 │       535 │      0 │  2446 │   7.6175 │
│ 010-response.json │   2308 │       734 │      0 │  3042 │   7.6352 │
│ 011-response.json │   2750 │       972 │      0 │  3722 │  12.2852 │
│ 012-response.json │   3517 │       800 │      0 │  4317 │   7.0031 │
│ 013-response.json │   2814 │      1313 │      0 │  4127 │  25.3103 │
│ 014-response.json │   3922 │       810 │      0 │  4732 │   6.5392 │
│ 015-response.json │   2824 │      1200 │      0 │  4024 │  14.8807 │
│ 016-response.json │   3817 │       820 │      0 │  4637 │   6.7683 │
│ TOTAL             │  47548 │     14635 │      0 │ 62183 │ 166.6962 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 95.92 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 5           │ 89.80 │
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
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 91.84 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 6           │ 87.76 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 007-py_04-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 91.84 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 6           │ 87.76 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 008-py_05-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 95.92 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 6           │ 87.76 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 010-py_06-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 8           │ 83.67 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 13          │ 73.47 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 012-py_07-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 8           │ 83.67 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 9           │ 81.63 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 014-py_08-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 95.92 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 95.92 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                        Code File: 016-py_09-test                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 016-py_09-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
