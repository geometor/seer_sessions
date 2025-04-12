
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

Okay, I will analyze the task examples provided.

**Perception of the Elements:**

1.  **Grid Structure:** Both input and output are 2D grids of pixels with integer values representing colors. The background is consistently white (0).
2.  **Objects:** Each input grid contains a single, contiguous, non-white rectangular object.
    *   Example 1: A 3x3 green (3) square.
    *   Example 2: A 6x5 red (2) rectangle.
3.  **Transformation:** The transformation involves adding a line segment (either horizontal or vertical) that starts from the boundary of the original object and extends towards one edge of the grid. The original object remains unchanged.
4.  **Color Consistency:** The added line segment always has the same color as the original object.
5.  **Directionality:**
    *   Example 1 (Grid 5x14 - wider than tall): The line extends horizontally to the right from the middle row of the object.
    *   Example 2 (Grid 14x7 - taller than wide): The line extends vertically downwards from the middle column of the object.
6.  **Rule Determination:** The direction of the extension (horizontal vs. vertical) appears to be determined by the aspect ratio of the *grid*, not the object. If the grid is wider than tall, the extension is horizontal. If the grid is taller or square, the extension is vertical.
7.  **Line Origin:** The line starts adjacent to the object's boundary.
    *   Horizontal line: Starts in the column immediately to the right of the object (`max_col + 1`) along the object's middle row.
    *   Vertical line: Starts in the row immediately below the object (`max_row + 1`) along the object's middle column.
8.  **Line Termination:** The line extends fully to the corresponding edge of the grid (right edge for horizontal, bottom edge for vertical).
9.  **Midpoint Calculation:** The "middle" row/column seems to be calculated using integer division of the sum of the min and max row/column indices of the object's bounding box.

**YAML Fact Sheet:**


```yaml
task_context:
  grid_representation: 2D array of integers (0-9) representing colors.
  background_color: white (0)
  input_features:
    - contains_single_object: true
    - object_is_contiguous: true
    - object_color_is_non_white: true
  output_features:
    - retains_original_object: true
    - adds_line_segment: true
    - line_color_matches_object: true
    - grid_dimensions_unchanged: true

object_properties:
  - id: primary_object
    color: non-white (varies per example, e.g., green(3), red(2))
    shape: rectangle (can be square)
    location: defined by bounding box (min_row, max_row, min_col, max_col)
    derived_properties:
      - middle_row: (min_row + max_row) // 2
      - middle_column: (min_col + max_col) // 2

transformation_rule:
  condition: grid_aspect_ratio
  cases:
    - if: grid_width > grid_height
      action: draw_horizontal_line
      line_properties:
        start_row: primary_object.middle_row
        start_col: primary_object.max_col + 1
        end_col: grid_width - 1
        color: primary_object.color
    - if: grid_height >= grid_width
      action: draw_vertical_line
      line_properties:
        start_col: primary_object.middle_column
        start_row: primary_object.max_row + 1
        end_row: grid_height - 1
        color: primary_object.color

relationships:
  - element: added_line
    relation: extends_from
    target: primary_object
  - element: added_line_direction
    relation: determined_by
    target: grid_aspect_ratio
  - element: added_line_position
    relation: aligned_with
    target: primary_object_midpoint (row or column depending on direction)
  - element: added_line_color
    relation: same_as
    target: primary_object_color
```


**Natural Language Program:**

1.  Identify the single contiguous block of non-white pixels in the input grid. Determine its color (C) and bounding box (min_row, max_row, min_col, max_col).
2.  Determine the height (H) and width (W) of the input grid.
3.  Calculate the middle row index of the object: `mid_row = (min_row + max_row) // 2`.
4.  Calculate the middle column index of the object: `mid_col = (min_col + max_col) // 2`.
5.  Create a copy of the input grid to serve as the output grid.
6.  Compare the grid width (W) and height (H):
    *   **If W > H (grid is wider than tall):**
        *   Iterate through each column index `c` from `max_col + 1` up to `W - 1`.
        *   Set the pixel value at `(mid_row, c)` in the output grid to color C.
    *   **Else (if H >= W, grid is taller than or same height as width):**
        *   Iterate through each row index `r` from `max_row + 1` up to `H - 1`.
        *   Set the pixel value at `(r, mid_col)` in the output grid to color C.
7.  Return the modified output grid.
