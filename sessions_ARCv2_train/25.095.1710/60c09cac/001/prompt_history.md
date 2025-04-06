
## train_1

**input:**
```
0 0 8 0
0 8 5 5
0 0 0 5
0 0 0 0
```


**output:**
```
0 0 0 0 8 8 0 0
0 0 0 0 8 8 0 0
0 0 8 8 5 5 5 5
0 0 8 8 5 5 5 5
0 0 0 0 0 0 5 5
0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 3 0
0 7 7
0 0 0
```


**output:**
```
0 0 3 3 0 0
0 0 3 3 0 0
0 0 7 7 7 7
0 0 7 7 7 7
0 0 0 0 0 0
0 0 0 0 0 0
```

*   **Perception:** The task involves transforming a smaller input grid of numbers into a larger output grid. The output grid's dimensions (height and width) are exactly double those of the input grid. Each number (or color) present in a cell of the input grid appears as a 2x2 block of the same number in the corresponding scaled position within the output grid. Cells with the value 0 in the input also result in a 2x2 block of 0s in the output. This transformation is consistent across both examples, indicating a pixel scaling or nearest-neighbor upscaling operation by a factor of 2.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    transformation: scaling
    scale_factor: 2
    input_object:
      type: grid
      properties:
        - height: H
        - width: W
        - cells: list of list of integers
    output_object:
      type: grid
      properties:
        - height: 2 * H
        - width: 2 * W
        - cells: list of list of integers
    relationship:
      - type: cell_mapping
        description: Each cell (r, c) in the input grid with value V corresponds to a 2x2 block of cells in the output grid.
        output_block_top_left: (2 * r, 2 * c)
        output_block_cells: [(2*r, 2*c), (2*r+1, 2*c), (2*r, 2*c+1), (2*r+1, 2*c+1)]
        output_block_value: V
    background_value: 0
    ```


*   **Natural Language Program:**
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Create a new output grid with height 2*H and width 2*W, initialized with a default value (e.g., 0).
    3.  Iterate through each cell of the input grid, identified by its row index `r` (from 0 to H-1) and column index `c` (from 0 to W-1).
    4.  Get the value `V` from the input cell at `(r, c)`.
    5.  In the output grid, fill the 2x2 block of cells starting at row `2*r` and column `2*c` with the value `V`. Specifically, set the cells at `(2*r, 2*c)`, `(2*r+1, 2*c)`, `(2*r, 2*c+1)`, and `(2*r+1, 2*c+1)` to the value `V`.
    6.  Return the completed output grid.
