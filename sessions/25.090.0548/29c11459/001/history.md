
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0 7
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 5 7 7 7 7 7
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 5 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception

The input and output grids have the same dimensions. In the provided examples, the dimensions are 5x11. The core transformation appears to operate row by row.

1.  **Identify Target Rows:** The transformation specifically targets rows that contain exactly two non-white pixels, one located at the very beginning (column 0) and the other at the very end (last column) of the row. Rows that don't meet this criterion remain unchanged.
2.  **Horizontal Expansion:** Within a target row, the leftmost colored pixel expands horizontally to the right, filling the cells with its color. Simultaneously, the rightmost colored pixel expands horizontally to the left, filling cells with its color.
3.  **Midpoint Fill:** The expansion from both sides stops just before the horizontal midpoint of the row. The exact midpoint column is then filled with a gray pixel (color 5).
4.  **Example 1:** The green pixel (3) at (3, 0) expands right to (3, 4). The orange pixel (7) at (3, 10) expands left to (3, 6). The midpoint column (index 5) is filled with gray (5) at (3, 5).
5.  **Example 2:** The blue pixel (1) at (1, 0) expands right to (1, 4). The red pixel (2) at (1, 10) expands left to (1, 6). The midpoint column (index 5) is filled with gray (5) at (1, 5).

The transformation essentially creates a horizontal bar in the target rows, composed of two colored segments originating from the edges and meeting at a central gray divider.

## Facts


```yaml
task_type: pattern_completion
grid_properties:
  - dimensions: consistent between input and output (e.g., 5x11 in examples)
  - background_color: predominantly white (0)

objects:
  - type: colored_pixels
    properties:
      - location: specific row and column index
      - color: non-white (1-9)
      - count_per_row: typically two in affected rows
      - initial_position: column 0 (left edge) and last column (right edge) in affected rows
  - type: generated_segments
    properties:
      - color: inherited from edge pixels
      - orientation: horizontal
      - extent: from edge towards the center
  - type: central_divider
    properties:
      - color: gray (5)
      - location: exact horizontal midpoint column of the affected row
      - shape: single pixel in the affected row

actions:
  - name: identify_target_rows
    criteria:
      - count of non-white pixels is exactly 2
      - one non-white pixel is at column 0
      - the other non-white pixel is at the last column
  - name: expand_left_pixel
    direction: rightward
    color: same as the pixel at column 0
    endpoint: column before the midpoint
  - name: expand_right_pixel
    direction: leftward
    color: same as the pixel at the last column
    endpoint: column after the midpoint
  - name: place_divider
    color: gray (5)
    location: midpoint column

relationships:
  - input_output: Output grid is derived from the input grid by modifying specific rows.
  - row_transformation: Transformation is applied independently to each row based on its content.
  - color_inheritance: The expanded segments inherit the colors of the initial edge pixels.
  - midpoint_dependency: The placement of the gray divider and the endpoints of the expanded segments depend on the grid width (specifically, the calculated midpoint column).
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Iterate through each row of the input grid, from top to bottom.
3.  For the current row:
    a.  Count the number of non-white pixels in the row.
    b.  Check if the count is exactly 2.
    c.  If the count is 2, check if the first pixel (column 0) is non-white and the last pixel (column `width - 1`) is non-white.
    d.  If both conditions (b and c) are true:
        i.  Determine the color of the leftmost pixel (`left_color`) and the rightmost pixel (`right_color`).
        ii. Calculate the midpoint column index: `mid_col = floor((width - 1) / 2)`.
        iii. Fill the corresponding row in the output grid:
            -   From column 0 up to (but not including) `mid_col`, set pixels to `left_color`.
            -   Set the pixel at column `mid_col` to gray (5).
            -   From column `mid_col + 1` up to (and including) `width - 1`, set pixels to `right_color`.
    e.  If the conditions in step 3d are *not* met, copy the entire input row directly to the corresponding row in the output grid.
4.  Return the completed output grid.
