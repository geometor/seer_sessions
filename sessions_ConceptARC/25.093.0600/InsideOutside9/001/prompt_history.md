
## train_1

**input:**
```
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 4
0 4 0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 4 0 0 2 0 0 0 0 0
4 0 0 2 0 0 0 0 0 0 2 0 4 0 0 0
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 4 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 0 0 0
0 0 0 0 4 0
0 0 0 0 0 0
0 2 2 2 2 0
0 0 0 0 0 0
0 0 4 0 0 0
0 2 2 2 2 0
0 0 0 0 0 0
0 0 0 0 0 0
0 4 0 4 4 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 2 2 2 2 0
0 0 0 0 0 0
0 0 4 0 0 0
0 2 2 2 2 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

*   **Perception:** The task involves processing a 2D grid of integers. The primary values observed are 0, 2, and 4. The transformation seems to selectively change some '4's to '0's while leaving other '4's and all '0's and '2's unchanged. The key factor determining whether a '4' is preserved appears to be its position relative to the locations of the '2's in the grid. The '2's seem to define boundary lines, either horizontally (rows) or vertically (columns).

*   **Facts:**
    
```yaml
    task_elements:
      - object: grid
        description: A 2D array of integers.
        properties:
          - dimensions: variable (rows x columns)
          - values: integers, primarily 0, 2, 4
      - object: boundary_lines
        description: Lines (rows or columns) defined by the positions of the number 2.
        properties:
          - orientation: 'row' or 'column', determined by the dimension (row index or column index) that has fewer unique values among the cells containing '2'.
          - range: defined by the minimum and maximum index (row or column) containing '2's along the determined orientation.
      - object: target_value
        description: The number 4 in the input grid.
        properties:
          - position: row and column index (r, c)
      - object: background_value
        description: The number 0 in the grid.
      - object: boundary_value
        description: The number 2 in the grid.

    actions:
      - action: identify_boundaries
        actor: system
        inputs:
          - input grid
        outputs:
          - boundary orientation ('row' or 'column')
          - minimum boundary index (min_idx)
          - maximum boundary index (max_idx)
        logic: Find all cells containing '2'. Collect unique row indices (R) and column indices (C). If len(R) < len(C), orientation is 'row', min/max_idx based on R. Otherwise, orientation is 'column', min/max_idx based on C (defaulting to column if lengths are equal).
      - action: filter_values
        actor: system
        inputs:
          - input grid
          - boundary orientation
          - min_idx
          - max_idx
        outputs:
          - output grid
        logic: Iterate through the input grid. If a cell contains '4', check its position relative to the boundaries based on the orientation. If the relevant index (row index for 'row' orientation, column index for 'column' orientation) is strictly between min_idx and max_idx, keep the '4'. Otherwise, change the '4' to '0'. Keep all '0's and '2's as they are.

    relationships:
      - relationship: spatial_containment
        object1: target_value (4)
        object2: boundary_lines
        description: A '4' is preserved only if its position falls strictly between the minimum and maximum boundary lines defined by the '2's, according to the determined orientation. Otherwise, it is replaced by '0'.
      - relationship: identity
        object1: boundary_value (2)
        object2: output grid cell
        description: Cells containing '2' in the input remain '2' in the output.
      - relationship: identity
        object1: background_value (0)
        object2: output grid cell
        description: Cells containing '0' in the input remain '0' in the output.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Locate all cells in the input grid containing the value '2'.
    3.  Collect the set of unique row indices `R` and unique column indices `C` where the value '2' occurs.
    4.  Determine the boundary orientation: If the number of unique row indices (`len(R)`) is less than the number of unique column indices (`len(C)`), set the orientation to 'row' and find the minimum (`min_idx`) and maximum (`max_idx`) row index in `R`. Otherwise (if `len(C) <= len(R)`), set the orientation to 'column' and find the minimum (`min_idx`) and maximum (`max_idx`) column index in `C`.
    5.  Iterate through each cell `(r, c)` of the input grid.
    6.  If the value at `input[r][c]` is '4':
        a.  If the orientation is 'row', check if the row index `r` is strictly greater than `min_idx` and strictly less than `max_idx`. If this condition is FALSE, change the value in the output grid at `output[r][c]` to '0'.
        b.  If the orientation is 'column', check if the column index `c` is strictly greater than `min_idx` and strictly less than `max_idx`. If this condition is FALSE, change the value in the output grid at `output[r][c]` to '0'.
    7.  Return the final output grid.
