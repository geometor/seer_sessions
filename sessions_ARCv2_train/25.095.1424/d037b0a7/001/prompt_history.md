
## train_1

**input:**
```
0 2 0
7 0 8
0 0 0
```


**output:**
```
0 2 0
7 2 8
7 2 8
```


## train_2

**input:**
```
0 0 6
0 4 0
3 0 0
```


**output:**
```
0 0 6
0 4 6
3 4 6
```


## train_3

**input:**
```
4 0 0
0 2 0
0 0 0
```


**output:**
```
4 0 0
4 2 0
4 2 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are grids (matrices) of integers. In the examples, they are 3x3 grids.
2.  **Grid Cells:** Each cell contains a single digit (0-9). The digit '0' appears to represent an empty or background state. Non-zero digits represent distinct "colors" or "objects".
3.  **Transformation Pattern:** The transformation seems to operate column by column. Within each column, non-zero digits "propagate" or "fall" downwards, filling any '0' cells below them. This propagation continues until the bottom of the grid is reached or another non-zero digit is encountered in that column. The original non-zero digits remain in their positions.

**YAML Fact Documentation:**


```yaml
Task: Grid Transformation - Downward Propagation

Objects:
  - Input Grid: A 2D array of integers.
  - Output Grid: A 2D array of integers, derived from the Input Grid.
  - Cells: Individual elements within the grids, containing integer values.
  - Columns: Vertical sequences of cells in the grid.
  - Non-zero Values: Digits other than 0, representing active elements.
  - Zero Values: The digit 0, representing empty space.

Properties:
  - Grid Dimensions: Height and Width (e.g., 3x3 in the examples).
  - Cell Value: The integer contained within a cell.
  - Cell Position: Row and Column index (e.g., (row, col)).

Actions:
  - Iterate: Process the grid column by column.
  - Track: For each column, maintain the value of the most recently encountered non-zero cell above the current position.
  - Fill: If a cell contains a zero and there was a non-zero value encountered above it in the same column, replace the zero with that non-zero value.
  - Copy: Non-zero values from the input grid are preserved in their original positions in the output grid.

Relationships:
  - Vertical Propagation: Non-zero values influence the zero values directly below them within the same column.
  - Column Independence: The transformation in one column does not directly affect other columns, except through the initial state of the input grid.
  - State Dependency: The value assigned to a zero cell depends on the nearest non-zero cell located above it in the same column.
```


**Natural Language Program:**

1.  Create the output grid as a copy of the input grid.
2.  Iterate through each column of the grid, from left to right.
3.  For the current column, initialize a variable `last_non_zero_value` to 0.
4.  Iterate through each row of the current column, from top to bottom (row index `r` starting from 0).
5.  Examine the value of the cell in the input grid at the current row `r` and column `c`, let's call it `input_value`.
6.  If `input_value` is not 0, update `last_non_zero_value` to `input_value`.
7.  If `input_value` is 0 and `last_non_zero_value` is not 0, set the value of the cell in the output grid at row `r` and column `c` to `last_non_zero_value`.
8.  Continue this process for all cells in all columns.
9.  The final state of the output grid is the result.
