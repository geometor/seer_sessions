
## train_1

**input:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
```


## train_2

**input:**
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 4 0 0 4 0
```

*   **Perception**: The task involves identifying specific patterns (objects) in the input grid and adding new pixels to the output grid based on the location of these patterns. The input grids contain one or more 'U'-shaped objects composed of a single color (green, magenta, azure). The output grids are identical to the input grids, but with additional yellow pixels placed in the last row. The position of each new yellow pixel seems related to the horizontal position of a 'U' shape above it.

*   **YAML Facts**:
    
```yaml
    task_description: Identify specific 'U'-shaped objects and add a marker below each in the last row.
    
    objects:
      - type: pattern
        name: U_shape
        description: A 3-wide, 2-high pattern of a single non-white color (C) arranged as [[C, C, C], [C, 0, C]].
        attributes:
          - color: The color of the pixels forming the shape (e.g., green, magenta, azure).
          - position: Top-left coordinates (row, col) of the 3x2 bounding box.
          - center_column: The column index of the middle pixel in the top row of the U_shape.
    
    actions:
      - name: find_U_shapes
        input: input_grid
        output: list_of_U_shapes (including their center_column)
      - name: add_markers
        input: input_grid, list_of_U_shapes
        output: output_grid
        description: >
          For each U_shape found, add a yellow pixel (color 4) to the grid.
          The pixel is placed in the last row of the grid, at the column index corresponding to the center_column of the U_shape.
    
    relationships:
      - type: spatial
        description: >
          A yellow marker pixel is placed vertically below the horizontal center of each identified U_shape.
      - type: location
        description: The yellow marker pixels are always placed in the last row of the grid.
    
    constraints:
      - The original content of the input grid, apart from the added yellow pixels, is preserved in the output grid.
      - Only the specific 3x2 U_shape pattern triggers the addition of a marker.
      - The marker color is always yellow (4).
    
    grid_properties:
      - size: Variable height and width.
      - background: Typically white (0).
    ```


*   **Natural Language Program**:
    1.  Create a copy of the input grid to serve as the basis for the output grid.
    2.  Iterate through the input grid to locate all occurrences of the 'U' shape pattern. This pattern is defined as a 3-pixel wide, 2-pixel high block where:
        *   Row `r`, columns `c`, `c+1`, `c+2` contain the same non-white color `X`.
        *   Row `r+1`, column `c` contains color `X`.
        *   Row `r+1`, column `c+1` contains white (0).
        *   Row `r+1`, column `c+2` contains color `X`.
    3.  For each 'U' shape found starting at row `r` and column `c`:
        *   Identify the column index of the center of the 'U' shape's top row, which is `c+1`.
        *   Determine the index of the last row of the grid (grid height - 1).
        *   In the output grid copy, place a yellow pixel (color 4) at the cell located at (last row index, `c+1`).
    4.  Return the modified grid as the output.
