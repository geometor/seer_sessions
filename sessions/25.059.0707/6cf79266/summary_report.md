╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                       Task Summary                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
                            Task Responses                             
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃  total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   7859 │       591 │      0 │   8450 │  12.2280 │
│ 002-response.json │   8312 │       535 │      0 │   8847 │   7.8342 │
│ 003-response.json │   3317 │       423 │      0 │   3740 │   9.1890 │
│ 004-response.json │   3602 │       222 │      0 │   3824 │   4.1402 │
│ 005-response.json │   1473 │      8192 │      0 │   9665 │  68.9658 │
│ 006-response.json │   9461 │       482 │      0 │   9943 │   6.3361 │
│ 007-response.json │   1733 │      3206 │      0 │   4939 │  29.4387 │
│ 008-response.json │   4739 │       574 │      0 │   5313 │   6.6149 │
│ 009-response.json │   3317 │       541 │      0 │   3858 │   9.5107 │
│ 010-response.json │   3720 │       197 │      0 │   3917 │   3.5225 │
│ 011-response.json │   1447 │      1749 │      0 │   3196 │  20.9788 │
│ 012-response.json │   2990 │       797 │      0 │   3787 │   8.5827 │
│ 013-response.json │   3317 │       436 │      0 │   3753 │   7.4719 │
│ 014-response.json │   3612 │       668 │      0 │   4280 │   7.9354 │
│ 015-response.json │   1917 │      3867 │      0 │   5784 │  38.4561 │
│ 016-response.json │   4186 │      3838 │      0 │   8024 │  36.1169 │
│ 017-response.json │   7822 │       784 │      0 │   8606 │   7.3402 │
│ 018-response.json │   5579 │       792 │      0 │   6371 │   7.2294 │
│ TOTAL             │  78403 │     27894 │      0 │ 106297 │ 291.8915 │
└───────────────────┴────────┴───────────┴────────┴────────┴──────────┘
                       Code File: 002-py_01-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 18          │ 95.50 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 18          │ 95.50 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 18          │ 95.50 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 004-py_02-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 18          │ 95.50  │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 23          │ 94.25  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 006-py_03-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 9           │ 97.75 │
│ 2       │ ❌    │ ✅   │ ❌      │ ❌          │ 9           │ 97.75 │
│ 3       │ ❌    │ ✅   │ ❌      │ ❌          │ 18          │ 95.50 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                      Code File: 008-py_05-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ❌      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ❌      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 010-py_06-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 18          │ 95.50  │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 27          │ 93.25  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 014-py_09-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 129         │ 67.75 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 114         │ 71.50 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 114         │ 71.50 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 015-py_10-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 129         │ 67.75 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 114         │ 71.50 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 114         │ 71.50 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 017-py_12-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 126         │ 68.50 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 113         │ 71.75 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 115         │ 71.25 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 018-py_13-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 40          │ 90.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 48          │ 88.00 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 36          │ 91.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
