╔═══════════════════════════════════════════════════════════════════════════════════════════╗
║                                       Task Summary                                        ║
╚═══════════════════════════════════════════════════════════════════════════════════════════╝
                            Task Responses                            
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┓
┃ file              ┃ prompt ┃ candidate ┃ cached ┃ total ┃ Time (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━╇━━━━━━━━━━┩
│ 001-response.json │   3851 │       575 │      0 │  4426 │   9.6097 │
│ 002-response.json │   4286 │       353 │      0 │  4639 │   5.0599 │
│ 003-response.json │   2171 │       510 │      0 │  2681 │   8.2547 │
│ 004-response.json │   2542 │       542 │      0 │  3084 │  18.9879 │
│ 005-response.json │   1793 │      2699 │      0 │  4492 │  29.8483 │
│ 006-response.json │   4293 │       497 │      0 │  4790 │   6.8725 │
│ 007-response.json │   1746 │      2544 │      0 │  4290 │  24.3166 │
│ 008-response.json │   4087 │       426 │      0 │  4513 │   4.4718 │
│ 009-response.json │   1849 │       499 │      0 │  2348 │   7.9012 │
│ 010-response.json │   2210 │       254 │      0 │  2464 │   3.4197 │
│ 011-response.json │   1505 │      2525 │      0 │  4030 │  26.8502 │
│ 012-response.json │   3826 │       890 │      0 │  4716 │   9.7674 │
│ 013-response.json │   2139 │      2188 │      0 │  4327 │  23.3714 │
│ 014-response.json │   4123 │       327 │      0 │  4450 │   3.7923 │
│ 015-response.json │   1923 │       458 │      0 │  2381 │   7.6652 │
│ 016-response.json │   2243 │       288 │      0 │  2531 │   3.5421 │
│ 017-response.json │   1540 │      1113 │      0 │  2653 │  11.0879 │
│ 018-response.json │   2450 │       621 │      0 │  3071 │   7.2221 │
│ 019-response.json │   1872 │      1280 │      0 │  3152 │  11.7409 │
│ 020-response.json │   2947 │       812 │      0 │  3759 │ 463.4007 │
│ TOTAL             │  53396 │     19401 │      0 │ 72797 │ 687.1824 │
└───────────────────┴────────┴───────────┴────────┴───────┴──────────┘
                       Code File: 002-py_01-test                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 002-py_01-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 004-py_02-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 006-py_04-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
│ 3       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 007-py_05-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
│ 3       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                      Code File: 008-py_06-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
│ 3       │ ❌    │ ❌   │ ✅      │ ❌          │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                       Code File: 010-py_07-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 012-py_09-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 014-py_11-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 2       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
│ 3       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                       Code File: 016-py_12-train                        
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━┩
│ 1       │ ❌    │ ❌   │ ✅      │ ✅          │ N/A         │ 0.00   │
│ 2       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
│ 3       │ ✅    │ ✅   │ ✅      │ ✅          │ 0           │ 100.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴────────┘
                      Code File: 018-py_13-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 2       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 3       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
                      Code File: 020-py_14-train                       
┏━━━━━━━━━┳━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━┓
┃ Example ┃ match ┃ size ┃ palette ┃ color count ┃ diff pixels ┃ %    ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━┩
│ 1       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 2       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
│ 3       │ ❌    │ N/A  │ N/A     │ N/A         │ N/A         │ 0.00 │
└─────────┴───────┴──────┴─────────┴─────────────┴─────────────┴──────┘
