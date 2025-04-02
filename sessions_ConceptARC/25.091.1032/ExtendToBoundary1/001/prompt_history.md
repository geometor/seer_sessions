
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3 3 3 3
0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 2 2 2 2 2 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
0 0 0 2 0 0 0
```

*   **Perception:**
    *   The input grids contain a single, solid-colored rectangular object on a white background.
    *   The output grids are modifications of the input grids.
    *   The modification involves extending a line of the object's color either horizontally to the right edge or vertically to the bottom edge of the grid.
    *   In the first example, a 3x3 green square has its middle row extended horizontally to the right edge.
    *   In the second example, a 6x5 red rectangle (taller than wide) has its middle column extended vertically to the bottom edge.
    *   The direction of extension seems to depend on the aspect ratio of the object: horizontal extension for objects that are square or wider than tall, and vertical extension for objects taller than wide.
    *   The line being extended corresponds to the geometric middle row or column of the object. If there are two middle rows/columns, the one with the lower index (topmost for rows, leftmost for columns) seems to be chosen.

*   **Facts:**
    
```yaml
    task_type: object_modification
    
    elements:
      - role: background
        color: white
        properties: occupies most of the grid initially.
      - role: object
        count: 1
        properties:
          - contiguous block of a single non-white color
          - rectangular shape
          - has a height (H) and width (W)
          - has a bounding box (min_row, max_row, min_col, max_col)
          - has a specific color (e.g., green, red)
      - role: extension_line
        properties:
          - same color as the object
          - originates from the object's boundary
          - extends either horizontally to the right grid edge or vertically to the bottom grid edge
          - its position is determined by the object's center
    
    relationships:
      - type: aspect_ratio_determines_direction
        description: The relationship between the object's height (H) and width (W) determines the extension direction.
        condition_1: If H > W (taller than wide), extension is vertical.
        condition_2: If H <= W (square or wider than tall), extension is horizontal.
      - type: center_determines_line
        description: The specific line (row or column) to extend is determined by the object's geometric center.
        details:
          - If extending horizontally, use the middle row. Index: `min_row + floor((H - 1) / 2)`.
          - If extending vertically, use the middle column. Index: `min_col + floor((W - 1) / 2)`.
      - type: extension_origin_and_extent
        description: The extension starts from the object's boundary and continues to the grid's edge.
        details:
          - Horizontal: Starts at `max_col + 1` and goes to the last column index.
          - Vertical: Starts at `max_row + 1` and goes to the last row index.
    
    actions:
      - identify_object: Find the single non-white contiguous object, its color, and bounding box.
      - calculate_dimensions: Determine the object's height (H) and width (W).
      - compare_dimensions: Check if H > W.
      - determine_extension_parameters: Based on the comparison, decide the direction (horizontal/vertical) and the specific row/column index to extend.
      - perform_extension: Modify the input grid by filling the cells along the determined line from the object's edge to the grid's edge with the object's color.

    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the single contiguous block of non-white pixels (the object). Record its color, its minimum and maximum row indices (`min_row`, `max_row`), and its minimum and maximum column indices (`min_col`, `max_col`).
    3.  Calculate the object's height: `H = max_row - min_row + 1`.
    4.  Calculate the object's width: `W = max_col - min_col + 1`.
    5.  Compare the height and width.
    6.  If the height `H` is greater than the width `W`:
        a.  Calculate the index of the middle column to extend: `extend_col = min_col + floor((W - 1) / 2)`.
        b.  Iterate through rows `r` from `max_row + 1` to the last row index of the grid.
        c.  For each `r`, set the color of the pixel at `(r, extend_col)` in the output grid to the object's color.
    7.  Else (if the height `H` is less than or equal to the width `W`):
        a.  Calculate the index of the middle row to extend: `extend_row = min_row + floor((H - 1) / 2)`.
        b.  Iterate through columns `c` from `max_col + 1` to the last column index of the grid.
        c.  For each `c`, set the color of the pixel at `(extend_row, c)` in the output grid to the object's color.
    8.  Return the modified output grid.
