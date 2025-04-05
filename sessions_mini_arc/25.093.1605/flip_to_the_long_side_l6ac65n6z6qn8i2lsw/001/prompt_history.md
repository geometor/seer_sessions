
## train_1

**input:**
```
0 0 0 7 0
0 0 0 0 7
0 0 0 7 0
0 0 0 0 7
0 0 0 7 0
```


**output:**
```
0 0 0 0 7
0 0 0 7 0
0 0 0 0 7
0 0 0 7 0
0 0 0 0 7
```


## train_2

**input:**
```
6 0 6 0 0
0 6 0 6 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 6 0 6 0
6 0 6 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
8 0 0 0 0
0 9 0 0 0
8 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 8 0 0 0
9 0 0 0 0
0 8 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
0 3 0 0 0
3 0 0 0 0
0 6 0 0 0
3 0 0 0 0
0 0 0 0 0
```


**output:**
```
3 0 0 0 0
0 3 0 0 0
6 0 0 0 0
0 3 0 0 0
0 0 0 0 0
```

*   **Perception of Elements:** The task operates on 2D grids of integers. The input grid undergoes a transformation to produce the output grid. The transformation appears to be column-based, specifically involving swapping pairs of adjacent columns. The dimensions of the grid remain constant. The values within the cells are moved, but not altered.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: grid
        properties:
          - type: 2D array of integers
          - dimensions: variable (e.g., 5x5 in examples)
          - cells: contain non-negative integers
      - relationship: adjacency
        between: columns
        definition: Columns with indices `j` and `j+1` are adjacent.
      - action: swap_columns
        target: adjacent column pairs
        condition: Applies to pairs starting with an even index (0, 2, 4, ...)
        effect: The entire content of column `j` is exchanged with the entire content of column `j+1`.
    transformation_goal:
      - Rearrange the grid by systematically swapping adjacent pairs of columns.
    ```


*   **Natural Language Program:**
    1.  Iterate through the columns of the input grid using an index `j`, starting from 0 and incrementing by 2 in each step (i.e., process columns 0, 2, 4, ...).
    2.  For each index `j`, check if a subsequent column `j+1` exists within the grid boundaries.
    3.  If column `j+1` exists, swap the entire contents of column `j` with the entire contents of column `j+1`.
    4.  The resulting grid after performing all necessary swaps is the output.
