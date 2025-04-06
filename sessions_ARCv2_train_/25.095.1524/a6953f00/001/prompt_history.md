
## train_1

**input:**
```
7 5 8 2
8 0 4 7
1 6 4 7
8 9 6 9
```


**output:**
```
8 2
4 7
```


## train_2

**input:**
```
0 7 9
5 6 5
3 7 9
```


**output:**
```
0 7
5 6
```


## train_3

**input:**
```
5 8 8 9 2
8 0 5 6 5
7 7 2 2 9
5 5 1 7 4
3 3 8 7 7
```


**output:**
```
5 8
8 0
```

**Perception of the Elements:**

1.  **Input Data:** The input consists of a grid (matrix) of single-digit integers, presented as space-separated values on multiple lines. The dimensions (rows and columns) of the input grid vary across examples.
2.  **Output Data:** The output is always a 2x2 grid of single-digit integers, also presented as space-separated values on two lines.
3.  **Transformation:** The output grid appears to be a specific 2x2 subgrid extracted from the input grid.
4.  **Key Pattern:** The selection of the 2x2 subgrid seems dependent on the width (number of columns) of the input grid.
    *   The starting row for the subgrid is consistently the first row (index 0).
    *   The starting column depends on the parity of the input grid's width (W):
        *   If W is even, the starting column is `W // 2`.
        *   If W is odd, the starting column is `0`.
    *   The subgrid always spans 2 rows (from the starting row) and 2 columns (from the starting column).

**Facts:**


```yaml
task: extract_subgrid
description: Extracts a specific 2x2 subgrid from a larger input grid based on the input grid's width.

input_elements:
  - object: grid
    properties:
      - type: matrix of integers
      - dimensions: variable (rows H, columns W)
      - format: space-separated values per row, newline-separated rows

output_elements:
  - object: grid
    properties:
      - type: matrix of integers
      - dimensions: fixed (2 rows, 2 columns)
      - format: space-separated values per row, newline-separated rows

transformation:
  action: select_subgrid
  parameters:
    - source: input_grid
    - size: 2x2
    - start_row_index: 0
    - start_column_index:
        condition:
          - if: input_grid.width is even
            value: input_grid.width // 2
          - else:
            value: 0
  output: output_grid

relationships:
  - output_grid is a subgrid of input_grid.
  - The starting column of the subgrid depends on the parity of the input_grid's width.
  - The starting row is always 0.
  - The size of the output_grid is constant (2x2).
```


**Natural Language Program:**

1.  Parse the input string into a 2D grid (list of lists or equivalent) of integers.
2.  Determine the width (W) of the input grid (number of columns).
3.  Calculate the starting column index (C) for the subgrid:
    a. If W is an even number, set C = W / 2.
    b. If W is an odd number, set C = 0.
4.  Extract the 2x2 subgrid from the input grid starting at row index 0 and column index C. This subgrid consists of the elements at indices `[0][C]`, `[0][C+1]`, `[1][C]`, and `[1][C+1]`.
5.  Format the extracted 2x2 subgrid into the required output string format (two lines, space-separated values).
