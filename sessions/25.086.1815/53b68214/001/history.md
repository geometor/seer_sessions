
## train_1

**input:**
```
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
2 0 2 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0
```


## train_3

**input:**
```
1 1 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 1 0 0 0
```


**output:**
```
1 1 1 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 1 1 1 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 1 1
0 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   The task transforms an input grid into an output grid.
    *   The dimensions of the output grid are related to the dimensions of the input grid. Specifically, the output grid's height is equal to the input grid's width, and the output grid's width is equal to the input grid's width. The output grid is always square with side length equal to the input grid's width.
    *   The content of the output grid is derived from the input grid by repeating patterns found in the columns of the input grid.
    *   Each column in the input grid defines a vertical pattern. This pattern is repeated downwards to fill the corresponding column in the output grid, extending it to the required output height.

*   **Facts**:
    
```yaml
    task_type: grid_transformation
    input_grid:
      properties:
        - height: H_in (variable)
        - width: W_in (variable)
    output_grid:
      properties:
        - height: H_out = W_in
        - width: W_out = W_in
    transformation:
      type: column_pattern_repetition
      details:
        - For each column index `c` from 0 to `W_in - 1`:
            - Define a pattern `P_c` as the sequence of pixel values in column `c` of the input grid, from top to bottom (length `H_in`).
            - Fill column `c` of the output grid by repeating the pattern `P_c` vertically.
            - The pixel value at `output[r][c]` is determined by the element at index `r % H_in` in the pattern `P_c`.
    ```


*   **Natural Language Program**:
    1.  Determine the height (`H_in`) and width (`W_in`) of the input grid.
    2.  Calculate the dimensions of the output grid: height `H_out = W_in`, width `W_out = W_in`.
    3.  Create a new grid (the output grid) with dimensions `H_out` x `W_out`.
    4.  Iterate through each column index `c` from 0 to `W_out - 1`.
    5.  For the current column `c`, extract the vertical sequence of pixel values from the input grid: `pattern = [input_grid[row][c] for row in range(H_in)]`.
    6.  Iterate through each row index `r` from 0 to `H_out - 1`.
    7.  Calculate the index within the `pattern` to use for the current output cell: `pattern_index = r % H_in`.
    8.  Set the pixel value at `output_grid[r][c]` to the value found at `pattern[pattern_index]`.
    9.  After iterating through all columns and rows, return the completed output grid.
