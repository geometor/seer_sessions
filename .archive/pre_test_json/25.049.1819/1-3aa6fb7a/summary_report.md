                                       Response Report                                        
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃                   ┃           ┃           ┃           ┃           ┃            ┃     Total ┃
┃                   ┃    Prompt ┃ Candidate ┃     Total ┃    Cached ┃   Response ┃   Elapsed ┃
┃ Response File     ┃    Tokens ┃    Tokens ┃    Tokens ┃    Tokens ┃   Time (s) ┃       (s) ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 001-response.json │      1669 │       482 │      2151 │         0 │     0.0004 │    6.8523 │
│ 002-response.json │      3914 │      1262 │      5176 │         0 │     0.0002 │   15.3281 │
│ 003-response.json │      7589 │      2789 │     10378 │         0 │     0.0001 │   29.5768 │
│ 004-response.json │     12884 │      4296 │     17180 │         0 │     0.0003 │   63.4953 │
│ Total             │     26056 │      8829 │     34885 │         0 │     0.0010 │           │
└───────────────────┴───────────┴───────────┴───────────┴───────────┴────────────┴───────────┘
                         Code File: 002                          
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ FAILED │ True │ True    │ False       │ 3           │
│ 2       │ FAILED │ True │ True    │ False       │ 5           │
└─────────┴────────┴──────┴─────────┴─────────────┴─────────────┘
                         Code File: 003                          
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ FAILED │ True │ True    │ True        │ 4           │
│ 2       │ FAILED │ True │ True    │ False       │ 4           │
└─────────┴────────┴──────┴─────────┴─────────────┴─────────────┘
                         Code File: 004                          
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Example ┃ Status ┃ size ┃ palette ┃ color count ┃ diff pixels ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ 1       │ FAILED │ True │ True    │ False       │ 6           │
│ 2       │ FAILED │ True │ True    │ False       │ 7           │
└─────────┴────────┴──────┴─────────┴─────────────┴─────────────┘
