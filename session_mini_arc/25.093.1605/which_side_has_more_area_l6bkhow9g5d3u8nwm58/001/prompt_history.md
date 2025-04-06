
## train_1

**input:**
```
0 0 5 0 0
0 5 0 0 0
0 5 0 0 0
0 5 0 0 0
0 0 5 0 0
```


**output:**
```
0 1 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 5 0 0
0 0 0 5 0
0 0 0 5 0
0 0 0 5 0
0 0 5 0 0
```


**output:**
```
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 0 0
0 5 0 0 0
0 0 5 0 0
0 5 0 0 0
0 0 5 0 0
```


**output:**
```
0 1 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


## train_4

**input:**
```
0 0 5 0 0
0 0 5 0 0
0 0 0 5 0
0 0 5 0 0
0 0 5 0 0
```


**output:**
```
1 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

*   **Perception:** The task involves transforming a 5x5 input grid containing zeros and fives into a 5x5 output grid containing mostly zeros and a single one. The fives in the input grid form a connected shape. The position of the single '1' in the output grid appears to be determined by the horizontal positioning of the shape formed by the fives in the input grid. Specifically, the index of the leftmost column containing a '5' dictates the position of the '1' in the output's first row.

*   **Facts:**
    
```yaml
    task_elements:
      - item: input_grid
        properties:
          - type: grid
          - dimensions: 5x5
          - cells: contain integers 0 or 5
          - five_pattern: forms a connected shape
      - item: output_grid
        properties:
          - type: grid
          - dimensions: 5x5
          - cells: contain integers 0 or 1
          - content: mostly zeros with a single '1'
      - item: transformation_rule
        properties:
          - based_on: horizontal position of the '5' pattern in the input grid
          - specific_detail: determines the column index of the '1' in the first row of the output grid
    relationships:
      - input_grid determines output_grid
      - leftmost_column_with_five: The index of the leftmost column in the input grid containing a '5'.
      - output_one_position:
          - if leftmost_column_with_five == 1, the '1' is at (row=0, column=1)
          - if leftmost_column_with_five == 2, the '1' is at (row=0, column=0)
    actions:
      - find_leftmost_five: Identify the index of the first column (from left, starting at index 0) in the input grid that contains the value '5'.
      - generate_output: Create a 5x5 grid filled with zeros.
      - place_one: Based on the index found in 'find_leftmost_five', place a '1' at the corresponding position in the first row of the output grid ((0, 1) if index is 1, (0, 0) if index is 2).
    ```


*   **Natural Language Program:**
    1.  Create a new 5x5 grid, initialized entirely with zeros. This will be the output grid.
    2.  Scan the input grid column by column, starting from the leftmost column (index 0) and moving rightwards.
    3.  Determine the index of the first column encountered that contains at least one cell with the value '5'. Let this index be `leftmost_col_idx`.
    4.  Check the value of `leftmost_col_idx`:
        *   If `leftmost_col_idx` is 1, set the value of the cell at row 0, column 1 in the output grid to '1'.
        *   If `leftmost_col_idx` is 2, set the value of the cell at row 0, column 0 in the output grid to '1'.
    5.  Return the modified output grid.
