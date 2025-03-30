
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 1 8 8 8 1 8 8
8 8 8 8 8 8 8 8 1 8 8 8 1 8 8
8 8 8 8 8 8 8 8 1 8 8 8 1 8 8
8 8 8 8 8 8 8 8 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 1 1 1 1 1 8 8 6 8 8 8 8
8 8 8 1 8 6 8 1 8 8 6 8 8 8 8
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
8 8 8 1 8 6 8 1 8 8 6 8 8 8 8
8 8 8 1 1 1 1 1 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
8 8 8 8 8 6 8 8 1 1 1 1 1 8 8
8 8 8 8 8 6 8 8 1 8 6 8 1 8 8
6 6 6 6 6 6 6 6 1 6 6 6 1 6 6
8 8 8 8 8 6 8 8 1 8 6 8 1 8 8
8 8 8 8 8 6 8 8 1 1 1 1 1 8 8
8 8 8 8 8 6 8 8 8 8 6 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 8 8 8 1 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 1 8 6 8 1 8 8 8 8 8 8 8
6 6 6 1 6 6 6 1 6 6 6 6 6 6 6
8 8 8 1 8 6 8 1 8 8 8 8 8 8 8
8 8 8 1 1 1 1 1 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
8 8 8 8 8 6 8 8 8 8 8 8 8 8 8
```

*   **Perception:** The task involves identifying hollow square shapes made of blue pixels on an azure background. For each such shape, lines are drawn in magenta color along the central row and central column corresponding to the center of the hollow area inside the square. These lines replace only the background azure pixels, leaving the original blue pixels of the square intact.

*   **Facts:**
    
```yaml
    background_color: azure (8)
    objects:
      - type: hollow_square
        color: blue (1)
        properties:
          - shape: square frame
          - encloses: a region of background color pixels
    actions:
      - action: identify_objects
        target: hollow_square (blue)
      - action: find_inner_hole
        target: hollow_square (blue)
        output: region of background_color (azure) pixels
      - action: calculate_center
        target: inner_hole
        output: center_row_index, center_column_index
      - action: draw_lines
        color: magenta (6)
        on_grid: output_grid
        location:
          - horizontal: center_row_index
          - vertical: center_column_index
        condition: replace only background_color (azure) pixels
    relationships:
      - The magenta lines are determined by the center of the hole inside each blue hollow square.
      - The lines extend across the entire grid dimension (row or column).
      - The original blue pixels are preserved in the output.
    grid_properties:
      - size: Remains the same between input and output.
      - background: Primarily azure, with added magenta lines.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the initial output grid.
    2.  Scan the input grid to identify all distinct, contiguous objects composed of blue (1) pixels.
    3.  For each blue object identified:
        a.  Determine if the object forms a hollow square shape, meaning it completely encloses a single contiguous area of non-blue pixels.
        b.  Verify that the enclosed area (the hole) consists entirely of the background color, azure (8).
        c.  If the object is a hollow blue square with an azure hole:
            i.  Find the bounding box of the azure hole.
            ii. Calculate the row index of the horizontal center line of the hole's bounding box (e.g., `center_row = (min_row + max_row) // 2`).
            iii. Calculate the column index of the vertical center line of the hole's bounding box (e.g., `center_col = (min_col + max_col) // 2`).
            iv. Iterate through each cell in the `center_row` of the grid. If the cell in the *input* grid at `(center_row, col)` contains the background color (azure, 8), change the color of the corresponding cell in the *output* grid to magenta (6).
            v.  Iterate through each cell in the `center_col` of the grid. If the cell in the *input* grid at `(row, center_col)` contains the background color (azure, 8), change the color of the corresponding cell in the *output* grid to magenta (6).
    4.  Return the final modified output grid.
