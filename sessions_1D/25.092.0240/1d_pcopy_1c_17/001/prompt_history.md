
## train_1

**input:**
```
0 2 2 2 0 0 0 2 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 2 2 2 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 5 5 5 0 0 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 0 5 5 5 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids are mostly white (background).
    *   Each input contains a dominant color (red, yellow, or gray).
    *   The topmost non-white pixels in the input always form a contiguous horizontal line. Let's call this the "reference line".
    *   Below the reference line, there might be one or more isolated pixels of the same dominant color.
    *   In the output, the reference line remains unchanged.
    *   For rows below the reference line in the input that contain *at least one* pixel of the dominant color, the corresponding row segment in the output is filled entirely with the dominant color, matching the horizontal extent (column start and end) of the reference line.
    *   If a row below the reference line does not contain any pixel of the dominant color in the input, it remains unchanged in the output.
    *   Pixels outside the column range of the reference line are unaffected.

*   **Facts:**
    
```yaml
    task_context:
      - Grid Transformation: Modifying pixels based on spatial relationships and color identity.
      - Color Focus: Operations primarily concern one non-white color per example, determined by the topmost structure.
      - Background: White pixels (0) are treated as background and are generally not modified unless specifically filled.
    
    elements:
      - type: Reference Line
        description: The topmost contiguous horizontal sequence of non-white pixels in the input grid.
        properties:
          - color: The single non-white color of the pixels in the line (e.g., red, yellow, gray). Let's call this C.
          - row_index: The row where this line occurs. Let's call this R.
          - column_range: The start and end column indices of the line. Let's call this [min_col, max_col].
      - type: Trigger Pixel
        description: Any pixel in a row below R (row index > R) that has the color C.
        properties:
          - color: Must be color C.
          - row_index: Must be greater than R.
          - column_index: Any column index.
      - type: Affected Row Segment
        description: A horizontal segment in the output grid corresponding to a row that contained a Trigger Pixel in the input.
        properties:
          - color: All pixels in this segment are set to color C.
          - row_index: Same as the row index of the Trigger Pixel(s) in that row.
          - column_range: Spans from min_col to max_col (inclusive), matching the Reference Line's column range.
    
    relationships:
      - The Reference Line defines the target color (C) and the horizontal boundaries ([min_col, max_col]) for modifications in subsequent rows.
      - The presence of at least one Trigger Pixel in a row `r > R` activates the transformation for that row.
      - The transformation fills the Affected Row Segment in the output grid for row `r` using color C and column range [min_col, max_col].
    
    actions:
      - Identify: Find the Reference Line (topmost horizontal non-white segment). Extract its color C, row R, and column range [min_col, max_col].
      - Scan: Iterate through rows below R (r > R).
      - Check: For each row r, determine if any pixel has color C.
      - Fill: If a check is positive for row r, modify the output grid by setting pixels from (r, min_col) to (r, max_col) to color C.
      - Copy: Unmodified pixels (including the reference line, rows below R without trigger pixels, and pixels outside the [min_col, max_col] range) retain their original values from the input.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Scan the input grid row by row from top to bottom to find the first row containing any non-white pixels.
    3.  Identify the contiguous horizontal segment of non-white pixels in this first non-white row. This is the "reference line".
    4.  Record the color (C), the row index (R), the starting column index (min_col), and the ending column index (max_col) of the reference line.
    5.  Iterate through each row `r` below the reference line (i.e., for `r` from `R + 1` to the last row).
    6.  For the current row `r`, check if there exists *any* pixel in the input grid at `(r, c)` (for any column `c`) that has the color C.
    7.  If such a pixel exists in row `r`, then modify the output grid: set all pixels from column `min_col` to `max_col` (inclusive) in row `r` to color C.
    8.  If no pixel of color C exists in row `r` in the input, the row `r` in the output grid remains unchanged from the initial copy.
    9.  Return the modified output grid.
