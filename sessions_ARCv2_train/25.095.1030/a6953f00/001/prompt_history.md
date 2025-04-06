
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

*   **Perception of Task Elements:**
    *   The input is always a rectangular grid of single-digit integers. The grid dimensions vary across examples.
    *   The output is always a 2x2 grid of single-digit integers.
    *   The numbers in the output grid are directly taken from the input grid; no arithmetic operations seem to be involved.
    *   The output grid corresponds to a specific 2x2 subgrid within the input grid.
    *   The location of the selected 2x2 subgrid appears to depend on the dimensions of the input grid. Specifically, it seems to depend on whether both the number of rows and the number of columns are even.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: Input_Grid
        properties:
          - type: grid (matrix) of integers
          - dimensions: variable rows (R) and columns (C)
      - object: Output_Grid
        properties:
          - type: grid (matrix) of integers
          - dimensions: fixed 2x2
          - source: derived from Input_Grid
      - object: Grid_Dimensions
        properties:
          - rows: R (integer)
          - columns: C (integer)
          - row_parity: even or odd
          - column_parity: even or odd
      - object: Selected_Subgrid
        properties:
          - dimensions: 2x2
          - position: defined by top-left corner coordinates (row_start, col_start)
          - content: elements from Input_Grid

    relationships:
      - Output_Grid is identical to Selected_Subgrid.
      - Selected_Subgrid is a contiguous 2x2 block of cells from Input_Grid.
      - The position (row_start, col_start) of Selected_Subgrid depends on the parity of Input_Grid dimensions (R, C).

    actions:
      - Determine the dimensions (R, C) of the Input_Grid.
      - Check if R is even AND C is even.
      - If true (both dimensions are even):
          Set the top-left corner of the Selected_Subgrid to (row_start=0, col_start=C-2).
      - If false (at least one dimension is odd):
          Set the top-left corner of the Selected_Subgrid to (row_start=0, col_start=0).
      - Extract the 2x2 subgrid from Input_Grid starting at the determined (row_start, col_start).
      - Set Output_Grid to the extracted Selected_Subgrid.
    ```


*   **Natural Language Program:**
    1.  Obtain the input grid and determine its number of rows (R) and columns (C).
    2.  Evaluate if both R and C are even numbers.
    3.  If R and C are both even, identify the 2x2 subgrid located at rows 0 and 1, and columns C-2 and C-1 (the top-right 2x2 corner).
    4.  If the condition in step 2 is false (i.e., R is odd or C is odd or both are odd), identify the 2x2 subgrid located at rows 0 and 1, and columns 0 and 1 (the top-left 2x2 corner).
    5.  Construct the output grid using the elements from the identified 2x2 subgrid.
