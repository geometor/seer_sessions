
## train_1

**input:**
```
0 3 0 0 0
5 0 2 8 0
0 0 0 2 0
3 0 6 0 0
0 0 0 0 9
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
5 0 2 8 0
3 3 6 2 9
```


## train_2

**input:**
```
0 0 0 0 2
3 3 3 0 0
0 7 6 0 8
1 0 0 8 0
0 6 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 3 0 0 0
3 7 3 0 2
1 6 6 8 8
```


## train_3

**input:**
```
0 0 0 0 4
0 0 0 4 0
0 0 4 0 0
0 4 0 0 0
4 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
4 4 4 4 4
```


## train_4

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 5 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 5 0 0
```

Okay, I will analyze the provided examples and generate the requested deliverables.

**Perception of Task Elements:**

The task involves transforming a 2D grid of numbers. The primary elements are the grid itself, the numbers within the grid (specifically distinguishing between zero and non-zero values), and the columns of the grid. The transformation appears to simulate a form of "gravity" acting independently on each column. Non-zero numbers within a column fall downwards, maintaining their relative vertical order, until they stack up at the bottom of the column or on top of another non-zero number. The cells left empty by this movement are filled with zeros.

**YAML Facts:**


```yaml
Grid:
  type: 2D array of integers
  properties:
    - rows: integer (number of rows)
    - columns: integer (number of columns)
    - cells: contain integer values

Cell Values:
  type: Integer
  properties:
    - value: The specific integer in the cell.
    - is_zero: boolean (true if value is 0, false otherwise)
    - significance: 
        - 0 represents empty space.
        - Non-zero values represent objects subject to gravity.

Columns:
  type: Vertical subset of the grid
  properties:
    - index: The horizontal position of the column (0-based).
    - elements: List of cell values in the column from top to bottom.

Transformation:
  name: Columnar Gravity
  scope: Operates independently on each column.
  action:
    - Identify non-zero values within a column.
    - Preserve the top-to-bottom relative order of these non-zero values.
    - Relocate these non-zero values to the bottom-most available positions within the same column in the output grid.
    - Fill the remaining upper positions in the column with zeros.
  relationship: The final position of a non-zero number depends only on its original vertical position relative to other non-zero numbers within the same column and the grid height. It is independent of numbers in other columns.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled with zeros.
2.  Iterate through each column of the input grid, from left to right (index `c`).
3.  For the current column `c`:
    a.  Create an empty temporary list to store the non-zero numbers encountered in this column.
    b.  Iterate through the rows of the input grid from top to bottom (index `r`).
    c.  If the value at `input[r][c]` is not zero, append this value to the temporary list.
    d.  Determine the number of non-zero elements collected (`num_non_zeros = length of temporary list`).
    e.  Iterate through the rows of the output grid for the current column `c`, starting from the bottom row (`grid_height - 1`) and moving upwards for `num_non_zeros` steps.
    f.  Place the collected non-zero numbers from the temporary list (in their collected order) into these bottom cells of the output column `c`. Specifically, place the last element of the temporary list at the bottom-most row, the second-to-last element in the row above it, and so on.
4.  Return the completed output grid.
