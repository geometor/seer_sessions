
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 0
```


## train_2

**input:**
```
0 0 2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 2 2 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 7 7 7 0
```

*   **Perception**: The input and output are always 1-dimensional grids (1 row). Each input grid contains a single contiguous block of a non-white color (red or orange in the examples) surrounded by white pixels. The output grid has the same dimensions and contains the same non-white block, but shifted horizontally to the right. The background remains white. The amount of the shift appears consistent across examples. In each case, the non-white block moves 3 positions to the right.

*   **Facts**:
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D (1 row, variable columns)
    background_color: white (0)
    objects:
      - type: contiguous_block
        color: non-white (any color except 0)
        count: 1 per grid
        properties:
          - length
          - color
          - starting_column_index
    actions:
      - name: horizontal_shift
        target: contiguous_block
        direction: right
        magnitude: 3 positions
    constraints:
      - grid_dimensions_remain_constant
      - object_color_remains_constant
      - object_length_remains_constant
      - background_remains_white
    ```


*   **Natural Language Program**:
    1.  Identify the single contiguous block of non-white pixels in the input grid.
    2.  Determine the starting column index of this block.
    3.  Determine the color and length of this block.
    4.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
    5.  Calculate the new starting column index for the block by adding 3 to its original starting column index.
    6.  Place the identified block (with its original color and length) into the output grid, starting at the calculated new column index.
