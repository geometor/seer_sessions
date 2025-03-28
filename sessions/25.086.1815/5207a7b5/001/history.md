
## train_1

**input:**
```
0 0 5 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
8 8 5 6 0 0 0 0
8 8 5 6 0 0 0 0
8 8 5 0 0 0 0 0
8 8 5 0 0 0 0 0
8 8 0 0 0 0 0 0
8 8 0 0 0 0 0 0
8 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
0 0 0 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
8 8 8 5 6 6 0
8 8 8 5 6 0 0
8 8 8 5 6 0 0
8 8 8 5 0 0 0
8 8 8 5 0 0 0
8 8 8 0 0 0 0
8 8 8 0 0 0 0
8 8 0 0 0 0 0
8 8 0 0 0 0 0
8 0 0 0 0 0 0
8 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 5 6 6 6
8 8 8 8 5 6 6 0
8 8 8 8 5 6 6 0
8 8 8 8 5 6 0 0
8 8 8 8 5 6 0 0
8 8 8 8 5 0 0 0
8 8 8 8 5 0 0 0
8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0
8 8 8 0 0 0 0 0
8 8 8 0 0 0 0 0
8 8 0 0 0 0 0 0
8 8 0 0 0 0 0 0
8 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input grid contains a single vertical line object composed of gray pixels (5). The rest of the grid is white (0).
    *   The output grid preserves the original gray line.
    *   Two new shapes are added to the output grid: one made of azure pixels (8) to the left of the gray line, and one made of magenta pixels (6) to the right.
    *   Both new shapes originate from the top row of the gray line and extend downwards and outwards (left for azure, right for magenta).
    *   The shapes appear roughly triangular or stepped, defined by diagonal boundaries (slope -1).
    *   The size and extent of the azure shape seem related to the
