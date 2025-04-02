
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 3 3 3 3 2 3 3 3 3 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 4 8 4 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 4 4 8 4 4 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

## Perception

1.  **Grid Structure:** Both examples operate on grids containing a background color (white, 0) and distinct colored objects.
2.  **Input Objects:** The inputs feature two main types of objects relevant to the transformation:
    *   A horizontal line segment of a uniform color (green in train_1, yellow in train_2).
    *   A single pixel of a different color located directly above the *start* of the horizontal line (red in train_1, azure in train_2).
3.  **Output Objects:** The outputs retain the original horizontal line, but modify it and add pixels. A new vertical line segment, 3 pixels high, appears.
4.  **Transformation:** The core transformation seems to involve using the single pixel's color and the horizontal line's position to create the new vertical line.
5.  **Positional Relationship:**
    *   The vertical line in the output is centered horizontally at the midpoint of the input horizontal line.
    *   The vertical line in the output is centered vertically on the row containing the horizontal line.
    *   The color of the new vertical line matches the color of the single pixel found above the start of the horizontal line in the input.
6.  **Overwriting:** The new vertical line overwrites any pixels previously at its location, including the pixel at the midpoint of the original horizontal line.
7.  **Multiple Instances:** Example train_2 shows that this transformation applies independently to multiple occurrences of the pattern within the same grid.

## Facts


```yaml
# Common Properties
grid_dimensions:
  - input_height == output_height
  - input_width == output_width
background_color: 0 # white

# Objects and Their Properties
objects:
  - type: horizontal_line
    description: A contiguous sequence of pixels of the same non-white color in a single row.
    properties:
      - color (line_color)
      - row_index (line_row)
      - start_column_index (start_col)
      - end_column_index (end_col)
      - length (end_col - start_col + 1)
      - midpoint_column_index (floor((start_col + end_col) / 2))
  - type: marker_pixel
    description: A single pixel located one row above the start_column_index of a horizontal_line.
    properties:
      - color (marker_color)
      - row_index (line_row - 1)
      - column_index (start_col)
  - type: vertical_line_output
    description: A vertical line segment, 3 pixels high, created in the output.
    properties:
      - color (derived from marker_color)
      - column_index (derived from horizontal_line midpoint)
      - top_row_index (line_row - 1)
      - center_row_index (line_row)
      - bottom_row_index (line_row + 1)

# Relationships and Actions
transformation:
  - action: find_all
    target: horizontal_line objects in the input grid.
  - action: for_each
    target: identified horizontal_line
    sub_actions:
      - action: locate
        target: marker_pixel
        condition: pixel exists at (line_row - 1, start_col)
        outputs:
          - marker_color
      - action: calculate
        input: start_col, end_col
        operation: floor((start_col + end_col) / 2)
        outputs:
          - midpoint_col
      - action: draw_vertical_line
        target: output grid
        parameters:
          - column: midpoint_col
          - top_row: line_row - 1
          - center_row: line_row
          - bottom_row: line_row + 1
          - color: marker_color
        effect: Overwrites existing pixels at these three locations.
  - action: preserve
    target: All other pixels from the input grid are copied to the output grid unless overwritten by the draw_vertical_line action.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each row of the input grid to identify the start of any potential horizontal line segments (a non-white pixel preceded by a white pixel or grid edge).
3.  For each potential start found at `(row, start_col)` with color `line_color`:
    a.  Determine the end column `end_col` of this contiguous horizontal line segment of `line_color`.
    b.  Check the pixel at `(row - 1, start_col)`. If this pixel exists (i.e., `row > 0`) and is not white (color 0), record its color as `marker_color`.
    c.  If a valid `marker_color` was found:
        i.  Calculate the midpoint column index: `mid_col = floor((start_col + end_col) / 2)`.
        ii. Modify the output grid:
            *   Set the pixel at `(row - 1, mid_col)` to `marker_color`.
            *   Set the pixel at `(row, mid_col)` to `marker_color`.
            *   Set the pixel at `(row + 1, mid_col)` to `marker_color` (ensure `row + 1` is within grid bounds).
4.  Return the modified output grid.
