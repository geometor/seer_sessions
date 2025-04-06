
## train_1

**input:**
```
0 0 0 0 0 9
0 0 0 8 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
4 0 7 8 0 0
4 0 7 8 0 9
```


## train_2

**input:**
```
0 4 0 9
0 0 0 0
0 4 6 0
1 0 0 0
```


**output:**
```
0 0 0 0
0 0 0 0
0 4 0 0
1 4 6 9
```


## train_3

**input:**
```
0 0 0 1 0
0 3 0 0 0
0 3 0 1 2
6 0 0 0 0
0 3 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 3 0 0 0
0 3 0 1 0
6 3 0 1 2
```

Okay, let's analyze the task based on the provided examples.

## Perception of Task Elements

1.  **Input/Output:** Both input and output are represented as 2D grids (matrices) containing single-digit non-negative integers.
2.  **Core Transformation:** The transformation appears to simulate a "gravity" effect acting vertically within each column independently.
3.  **Number Movement:** Non-zero numbers within each column "fall" downwards towards the bottom row.
4.  **Zero Handling:** Zeroes (0) seem to act as empty space, allowing numbers to fall through them.
5.  **Collision/Stacking:** When a falling number encounters another non-zero number below it (or the grid floor), it stops in the cell immediately above the obstacle/floor.
6.  **Order Preservation:** The relative vertical order of the non-zero numbers within a single column is preserved after they fall. Numbers originally higher up in a column will still be higher up relative to numbers originally lower in the same column, once they have all settled at the bottom.
7.  **Independence:** The process applied to one column does not seem to directly affect the numbers or their final positions in other columns.

## Facts


```yaml
Context: Grid Transformation Task

Objects:
  - name: Grid
    properties:
      - rows: Integer (number of rows)
      - columns: Integer (number of columns)
      - cells: List[List[Cell]]
  - name: Cell
    properties:
      - row_index: Integer
      - column_index: Integer
      - value: Integer (0-9)
  - name: Number
    properties:
      - value: Integer (1-9) # Non-zero value
      - initial_position: Tuple[Integer, Integer] # (row, column)
      - final_position: Tuple[Integer, Integer] # (row, column)
  - name: Column
    properties:
      - index: Integer
      - cells: List[Cell]
      - non_zero_values: List[Integer] # Ordered list of non-zero values from top to bottom

Relationships:
  - Grid contains Columns.
  - Grid contains Cells.
  - Columns contain Cells.
  - Numbers occupy Cells (at initial and final positions).

Actions:
  - Identify non-zero numbers within each column.
  - Determine the final resting position for each non-zero number based on gravity.
  - Reconstruct the output grid column by column.

Rule:
  - For each column in the input grid:
    1. Extract all non-zero numbers, preserving their top-to-bottom order.
    2. Create a new column of the same height, initially filled with zeros.
    3. Place the extracted non-zero numbers into the new column, starting from the bottom row and moving upwards, maintaining their preserved order.
  - Combine the newly created columns to form the output grid.
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with zeros.
2.  Get the number of rows (`num_rows`) and columns (`num_cols`) from the input grid.
3.  Iterate through each column index `c` from 0 to `num_cols - 1`.
4.  For the current column `c`:
    a.  Create an empty list called `column_numbers`.
    b.  Iterate through each row index `r` from 0 to `num_rows - 1`.
    c.  If the value in the input grid at `(r, c)` is not zero, append this value to the `column_numbers` list.
    d.  Determine the number of non-zero numbers found (`count = length of column_numbers`).
    e.  Iterate backwards from `k = count - 1` down to 0 (representing the index in `column_numbers`).
    f.  Calculate the target row index in the output grid: `target_row = num_rows - 1 - (count - 1 - k)`.
    g.  Place the number `column_numbers[k]` into the output grid at position (`target_row`, `c`).
5.  Return the completed output grid.
