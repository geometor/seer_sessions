
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 5 0 0 0 0
9 0 0 0 0 5 0 0 0 0
6 0 0 0 5 5 0 0 0 0
6 0 0 5 5 5 0 0 0 0
6 0 0 5 0 5 0 0 0 0
4 0 0 0 0 5 0 0 0 0
4 0 0 0 0 5 0 0 0 0
4 0 0 0 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 9 0 0 0 0
9 0 0 0 0 9 0 0 0 0
6 0 0 0 6 6 0 0 0 0
6 0 0 6 6 6 0 0 0 0
6 0 0 6 0 6 0 0 0 0
4 0 0 0 0 4 0 0 0 0
4 0 0 0 0 4 0 0 0 0
4 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 5 0 0 0 0
8 0 0 0 0 5 0 0 0 0
8 0 0 5 5 5 0 0 0 0
2 0 0 5 0 0 0 0 0 0
2 0 0 5 0 0 0 0 0 0
2 0 0 5 5 5 5 0 0 0
2 0 0 0 0 0 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 8 0 0 0 0
8 0 0 0 0 8 0 0 0 0
8 0 0 8 8 8 0 0 0 0
2 0 0 2 0 0 0 0 0 0
2 0 0 2 0 0 0 0 0 0
2 0 0 2 2 2 2 0 0 0
2 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, analyzing the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Data Structure:** The input and output are both 2D grids (matrices) of integers. The grid dimensions appear consistent between input and output within each example (10x10).
2.  **Key Values:** The grids contain the digit '0' (representing a background or empty state) and other non-zero digits. The digit '5' seems to play a special role in the input, as it is present in the input grids but absent in the output grids.
3.  **Transformation Pattern:** The core transformation involves replacing occurrences of the digit '5' in the input grid. The replacement value is determined by another digit within the *same row*. Specifically, the digit in the first column (column index 0) of that row seems to dictate the replacement value for any '5's found in that row.
4.  **Row-Based Logic:** The transformation appears to operate independently on each row. The value used for replacement is constant for all '5's within a single row.
5.  **Identity:** Digits other than '5' in the input seem to retain their original value and position in the output grid. The '0's also remain unchanged.

**Fact Document:**


```yaml
task_elements:
  - object: grid
    type: 2D array of integers
    role: input and output container
  - object: cell
    properties:
      - value: integer (0-9)
      - position: (row_index, column_index)
  - object: target_digit
    value: 5
    description: The specific digit in the input grid that undergoes replacement.
  - object: replacement_source
    location: Column 0 of each row in the input grid.
    description: The value in this column determines the replacement for the target_digit in the same row.
relationships:
  - type: governs
    subject: cell at (row, 0) in input grid
    object: all cells with value 5 in the same row 'row'
    description: The value of the cell at column 0 dictates the output value for cells containing '5' in that row.
actions:
  - name: replace
    actor: transformation process
    target: each cell in the input grid with value 5
    effect: change the cell's value in the output grid to the value found in column 0 of its corresponding row in the input grid.
  - name: copy
    actor: transformation process
    target: each cell in the input grid with value != 5
    effect: maintain the cell's original value in the output grid.
```


**Natural Language Program:**

1.  Initialize an empty output grid with the same dimensions as the input grid.
2.  Iterate through each row of the input grid, identified by its row index `r`.
3.  For the current row `r`, determine the replacement value by reading the digit located at column index 0 (i.e., `input_grid[r][0]`). Store this as `replacement_value`.
4.  Iterate through each column of the current row `r`, identified by its column index `c`.
5.  Examine the value of the cell at `input_grid[r][c]`.
6.  If the value of `input_grid[r][c]` is 5, set the corresponding cell in the output grid, `output_grid[r][c]`, to the `replacement_value` determined in step 3.
7.  If the value of `input_grid[r][c]` is *not* 5, copy the value directly from the input to the output: set `output_grid[r][c]` to `input_grid[r][c]`.
8.  After iterating through all rows and columns, the output grid contains the transformed result.
