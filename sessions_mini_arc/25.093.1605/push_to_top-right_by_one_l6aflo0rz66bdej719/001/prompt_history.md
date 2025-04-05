
## train_1

**input:**
```
1 8 3 4 4
0 1 8 3 4
0 0 1 8 3
0 0 0 1 8
0 0 0 0 1
```


**output:**
```
0 1 8 3 4
0 0 1 8 3
0 0 0 1 8
0 0 0 0 1
4 0 0 0 0
```


## train_2

**input:**
```
1 7 4 5 5
0 1 7 4 5
0 0 1 7 4
0 0 0 1 7
0 0 0 0 1
```


**output:**
```
0 1 7 4 5
0 0 1 7 4
0 0 0 1 7
0 0 0 0 1
5 0 0 0 0
```


## train_3

**input:**
```
1 3 3 3 3
0 1 3 3 3
0 0 1 3 3
0 0 0 1 3
0 0 0 0 1
```


**output:**
```
0 1 3 3 3
0 0 1 3 3
0 0 0 1 3
0 0 0 0 1
3 0 0 0 0
```


## train_4

**input:**
```
1 2 4 8 8
0 1 2 4 8
0 0 1 2 4
0 0 0 1 2
0 0 0 0 1
```


**output:**
```
0 1 2 4 8
0 0 1 2 4
0 0 0 1 2
0 0 0 0 1
8 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are both square grids (matrices) of integers, specifically 5x5 in all examples.
    *   The input grids have a distinct upper-triangular-like structure, with 1s on the main diagonal and 0s below it. The values above the diagonal vary.
    *   The transformation involves a manipulation of the rows.
    *   Comparing input and output grids reveals that rows 2 through 5 of the input seem to directly correspond to rows 1 through 4 of the output. This suggests a row-shifting operation.
    *   The first row of the input is discarded in this shift.
    *   The last row of the output is newly constructed and does not directly copy any single row from the input. It consists of a single non-zero number in the first column, followed by zeros.
    *   The non-zero value in the first column of the output's last row appears to be derived from the input grid. Specifically, it matches the value found in the last column of the *first* row of the input grid.

*   **Facts:**
    
```yaml
    objects:
      - grid:
          properties:
            - rows: list of rows
            - dimensions: N x N (e.g., 5x5)
      - row:
          properties:
            - elements: list of integers
            - index: integer (position in the grid)
      - cell:
          properties:
            - value: integer
            - position: (row_index, column_index)
    actions:
      - copy_rows:
          source: input grid
          target: output grid
          details: Rows 2 to N of the input are copied to rows 1 to N-1 of the output.
      - extract_value:
          source: input grid
          position: (row 1, column N)
          target_variable: first_element_of_last_row
      - construct_row:
          target: output grid
          row_index: N (last row)
          elements:
            - element 1: value from extract_value step
            - elements 2 to N: set to 0
    relationships:
      - output rows 1 to N-1 are identical to input rows 2 to N.
      - output row N, column 1 value is identical to input row 1, column N value.
      - output row N, columns 2 to N values are always 0.
    ```


*   **Natural Language Program:**
    1.  Identify the input grid and its dimensions (N x N).
    2.  Create a new output grid of the same dimensions (N x N).
    3.  Copy rows 2 through N from the input grid into rows 1 through N-1 of the output grid, maintaining their relative order.
    4.  Extract the value located at row 1, column N of the input grid.
    5.  Construct the Nth (last) row of the output grid:
        *   Set the element in the first column (column 1) to the value extracted in step 4.
        *   Set all elements from the second column (column 2) through the Nth column (column N) to 0.
    6.  Return the completed output grid.
