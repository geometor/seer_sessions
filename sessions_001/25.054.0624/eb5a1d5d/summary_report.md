┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                        Task Summary                                        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                            Task Responses                             
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃  total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   3009 │       648 │      0 │   3657 │   9.5009 │
│ 002-response.json │   3517 │       478 │      0 │   3995 │   5.7402 │
│ 003-response.json │   5573 │      7227 │      0 │  12800 │  60.9845 │
│ 004-response.json │   7102 │      1146 │      0 │   8248 │  12.1485 │
│ 005-response.json │   8038 │       554 │      0 │   8592 │   5.9961 │
│ 006-response.json │  12597 │       486 │      0 │  13083 │   5.5421 │
│ 007-response.json │   2835 │       453 │      0 │   3288 │   7.5953 │
│ 008-response.json │   3148 │       314 │      0 │   3462 │   4.0610 │
│ 009-response.json │   5312 │       986 │      0 │   6298 │  12.2047 │
│ 010-response.json │   6093 │      1056 │      0 │   7149 │  11.7537 │
│ 011-response.json │   6959 │      3545 │      0 │  10504 │  32.1170 │
│ 012-response.json │  10297 │       712 │      0 │  11009 │   7.4795 │
│ 013-response.json │   2739 │       631 │      0 │   3370 │   9.2948 │
│ 014-response.json │   3233 │       482 │      0 │   3715 │   6.1626 │
│ 015-response.json │   5721 │      1301 │      0 │   7022 │  16.0306 │
│ 016-response.json │   6815 │      1134 │      0 │   7949 │  11.3325 │
│ 017-response.json │   9344 │      1041 │      0 │  10385 │  14.2662 │
│ 018-response.json │  10181 │      1817 │      0 │  11998 │  15.7036 │
│ TOTAL             │ 112513 │     24011 │      0 │ 136524 │ 247.9137 │
└───────────────────┴────────┴───────────┴────────┴────────┴──────────┘
                       Code File: 002-py_01-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                                  Code File: 003-py_02-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                       Code File: 005-py_03-test                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 005-py_03-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 006-py_04-test                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 006-py_04-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 008-py_05-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                      Code File: 010-py_06-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                                  Code File: 011-py_07-train                                  
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━┓
┃ Example             ┃ match               ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ % ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━┩
│ Code Execution      │ transform function  │      │         │             │             │   │
│ Error               │ not found           │      │         │             │             │   │
└─────────────────────┴─────────────────────┴──────┴─────────┴─────────────┴─────────────┴───┘
                      Code File: 012-py_08-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 014-py_09-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 2       │ ❌    │ ❌   │ ❌      │ ❌          │ N/A         │ 0.00   │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                      Code File: 016-py_10-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                      Code File: 018-py_11-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
