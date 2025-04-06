
## train_1

**input:**
```
0 4 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
0 4 0 0 0 0 0
4 0 4 0 0 0 0
```


## train_2

**input:**
```
0 2 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
```

## Perception of Elements

1.  **Input/Output Format**: Both input and output are 2D grids (or matrices) of integers. The examples show grids with 6 rows. The number of columns varies (7 in the first, 10 in the second).
2.  **Key Feature**: The transformation primarily involves the non-zero numbers present only in the *first row* of the input grid. All other rows in the input are filled with zeros.
3.  **Transformation Pattern**: Each non-zero number `v` found at column `c` in the first row (`row 0`) of the input propagates downwards through the subsequent rows.
    *   The propagation pattern alternates based on the row index `r` (starting from `r=1`).
    *   In **odd-numbered rows** (`r = 1, 3, 5, ...`), the value `v` appears in the columns immediately to the left (`c-1`) and right (`c+1`) of the original column `c`, provided these columns exist within the grid boundaries.
    *   In **even-numbered rows** (`r = 2, 4, ...`), the value `v` appears directly below the original position, in the same column `c`.
4.  **Independence**: The propagation of each non-zero value from the first row occurs independently. The final output grid is a combination of the original first row and the propagated values in the subsequent rows.
5.  **Value Preservation**: The numeric value of the propagating number remains the same throughout the process.
6.  **Grid Initialization**: The output grid retains the initial non-zero values from the first row of the input. The subsequent rows are initially considered empty (or zero-filled) and then populated according to the propagation rule.

## YAML Facts


```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D array of integers
      - role: input and output container
      - dimensions: variable columns, fixed rows (in examples)
  - element: Cell
    properties:
      - type: integer value (0 or non-zero)
      - location: defined by row and column index
  - element: Initial Value
    properties:
      - type: non-zero integer
      - location: confined to the first row (row 0) of the input grid
      - role: seed for propagation
relationships:
  - type: Propagation
    source: Initial Value at (0, c)
    target: Cells in subsequent rows (r > 0)
    rule:
      - condition: row r is odd
        action: Place value at (r, c-1) and (r, c+1), if columns are valid
      - condition: row r is even
        action: Place value at (r, c)
    properties:
      - value is preserved
      - each initial value propagates independently
actions:
  - action: Identify Initial Values
    inputs: input grid (first row)
    outputs: list of (value, column_index) pairs for non-zero cells
  - action: Propagate Value Downwards
    inputs: (value, column_index) from first row, grid dimensions
    outputs: populated cells in rows 1 to num_rows-1 according to the alternating pattern
  - action: Combine Results
    inputs: original input grid, propagated values
    outputs: final output grid
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each cell `(0, c)` in the first row (`row 0`) of the input grid.
3.  If the cell `(0, c)` contains a non-zero value `v`:
    a.  Iterate through the subsequent rows `r` from 1 down to the last row of the grid.
    b.  If the current row index `r` is **odd**:
        i.  If the column `c-1` is within the grid's left boundary (`c-1 >= 0`), set the value of the cell `(r, c-1)` in the output grid to `v`.
        ii. If the column `c+1` is within the grid's right boundary (`c+1 < number_of_columns`), set the value of the cell `(r, c+1)` in the output grid to `v`.
    c.  If the current row index `r` is **even**:
        i.  Set the value of the cell `(r, c)` in the output grid to `v`.
4.  Return the modified output grid.
