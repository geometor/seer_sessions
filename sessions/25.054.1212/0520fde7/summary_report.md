┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   1777 │       581 │      0 │  2358 │   9.3553 │
│ 002-response.json │   2220 │       249 │      0 │  2469 │   3.4339 │
│ 003-response.json │   1998 │      1556 │      0 │  3554 │  16.1037 │
│ 004-response.json │   1874 │       990 │      0 │  2864 │  13.3306 │
│ 005-response.json │   2661 │       325 │      0 │  2986 │   3.9575 │
│ 006-response.json │   3349 │       426 │      0 │  3775 │   4.5407 │
│ 007-response.json │   1777 │       514 │      0 │  2291 │   7.3966 │
│ 008-response.json │   2153 │       441 │      0 │  2594 │   4.6537 │
│ 009-response.json │   2190 │      1090 │      0 │  3280 │  13.8450 │
│ 010-response.json │   3074 │       483 │      0 │  3557 │   4.8558 │
│ 011-response.json │   2232 │      1214 │      0 │  3446 │  14.1493 │
│ 012-response.json │   3241 │       454 │      0 │  3695 │  22.9767 │
│ 013-response.json │   1777 │       732 │      0 │  2509 │   9.6380 │
│ 014-response.json │   2371 │       523 │      0 │  2894 │   4.9451 │
│ 015-response.json │   2272 │      2838 │      0 │  5110 │  27.9837 │
│ 016-response.json │   2398 │      1171 │      0 │  3569 │  14.4244 │
│ 017-response.json │   3365 │       548 │      0 │  3913 │   5.5759 │
│ 018-response.json │   4904 │       904 │      0 │  5808 │   7.1002 │
│ TOTAL             │  45633 │     15039 │      0 │ 60672 │ 188.2661 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 55.56  │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 3           │ 66.67  │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                                  Code File: 003-py_02-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                      Code File: 005-py_03-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 006-py_04-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 77.78 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 77.78 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 5           │ 44.44 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 008-py_05-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 77.78 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 77.78 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 5           │ 44.44 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 010-py_06-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 1           │ 88.89 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 3           │ 66.67 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 77.78 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 012-py_07-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 77.78 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 6           │ 33.33 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 3           │ 66.67 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 014-py_08-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 77.78 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 3           │ 66.67 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 55.56 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                                  Code File: 015-py_09-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                       Code File: 017-py_10-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ❌          │ 2           │ 77.78 │
│ 2       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 77.78 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 5           │ 44.44 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
                       Code File: 018-py_11-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %     ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━┩
│ 1       │ ❌    │ ✅   │ ✅      │ ✅          │ 2           │ 77.78 │
│ 2       │ ❌    │ ✅   │ ✅      │ ❌          │ 3           │ 66.67 │
│ 3       │ ❌    │ ✅   │ ✅      │ ❌          │ 4           │ 55.56 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴───────┘
