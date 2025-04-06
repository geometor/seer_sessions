
## train_1

**input:**
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```


## train_2

**input:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```


**output:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```

*   **Perception**: The task operates on grids of numbers. The input grid has a distinct pattern where the top rows contain non-zero numbers, and the remaining rows are filled with zeros. The output grid retains the top non-zero rows from the input and also places a vertically mirrored copy of these non-zero rows at the very bottom, overwriting the original zero rows in those positions. The dimensions of the grid remain unchanged.

*   **YAML Facts**:
    
```yaml
    task_type: grid_transformation
    input_object:
      type: grid
      element_type: integer
      properties:
        - height: variable (e.g., 10 in examples)
        - width: variable (e.g., 5 or 3 in examples)
        - structure: contains a block of non-zero rows at the top, followed by zero rows.
    output_object:
      type: grid
      element_type: integer
      properties:
        - height: same as input height
        - width: same as input width
        - structure: contains the original top non-zero rows, followed by zero rows, and concluding with a vertically mirrored copy of the top non-zero rows.
    transformation:
      action: copy_and_mirror
      elements_involved:
        - source: non-zero rows from the top of the input grid
        - target: bottom rows of the output grid
      relationship:
        - The number of non-zero rows at the top determines the number of rows mirrored at the bottom.
        - The original content of the input grid is preserved in the output, except for the bottom rows which are replaced by the mirrored block.
    ```


*   **Natural Language Program**:
    1.  Identify the contiguous block of rows starting from the top row (row 0) of the input grid that contain at least one non-zero element. Let this block be `TopBlock`.
    2.  Determine the number of rows in `TopBlock`, let this be `N`.
    3.  Create a new grid, `OutputGrid`, with the same dimensions as the input grid.
    4.  Copy all rows from the input grid to the `OutputGrid`.
    5.  Create a reversed copy of the rows in `TopBlock`. Let this be `MirroredBlock`.
    6.  Replace the last `N` rows of the `OutputGrid` with the rows from `MirroredBlock`. Specifically, the first row of `MirroredBlock` replaces row `H-N` of `OutputGrid`, the second row of `MirroredBlock` replaces row `H-N+1`, and so on, until the last row of `MirroredBlock` replaces the last row (`H-1`) of `OutputGrid` (where `H` is the total height of the grid).
    7.  The final `OutputGrid` is the result.
