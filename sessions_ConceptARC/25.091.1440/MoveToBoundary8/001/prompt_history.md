
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 4 0 4 0 4 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 4 0 4 0 4 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception**

*   **Example 1 (train_1):**
    *   Input has a vertical green line segment and three yellow pixels horizontally aligned to the left of the line.
    *   Output shows the same green line, but the yellow pixels have shifted horizontally to the right. Each yellow pixel moved 4 steps to the right, maintaining its row.
*   **Example 2 (train_2):**
    *   Input has a horizontal red line segment and three azure pixels scattered below the line.
    *   Output shows the same red line, but the azure pixels have moved. Each azure pixel moved 5 steps up. Additionally, their horizontal position changed: pixels whose original column was outside or at the ends of the red line's column span moved 5 steps right; the pixel whose original column was strictly within the red line's span moved 3 steps right.

**Commonalities and Transformation Logic:**
1.  There is always a single static line object (vertical green or horizontal red).
2.  There are multiple point objects of a single color (yellow or azure) distinct from the line color.
3.  The point objects move relative to the static line.
4.  The primary direction of movement seems to be *towards* the line (rightwards towards the vertical line in train\_1, upwards towards the horizontal line in train\_2).
5.  There's a secondary movement component parallel to the line, which may depend on the point's position relative to the line's *span* (ends vs. interior).
    *   For the vertical line (train\_1), the secondary movement (vertical) was zero. All points moved right by 4.
    *   For the horizontal line (train\_2), the primary movement (vertical) was 5 steps up. The secondary movement (horizontal) was 5 steps right for points outside/at the ends of the line's span, and 3 steps right for points strictly within the span.

**Facts**


```yaml
task_description: Move point objects relative to a static line object based on orientation and position.

elements:
  - type: static_line
    properties:
      - color: (varies, e.g., green, red)
      - orientation: (horizontal or vertical)
      - position: (row index for horizontal, column index for vertical)
      - span: (min/max column for horizontal, min/max row for vertical)
  - type: moving_points
    properties:
      - color: (varies, e.g., yellow, azure)
      - count: (multiple)
      - initial_positions: (list of (row, col) tuples)

transformation:
  - action: identify_objects
    source: input_grid
    target: static_line, moving_points
  - action: determine_line_properties
    source: static_line
    target: orientation, position, span
  - action: determine_point_properties
    source: moving_points
    target: color, initial_positions
  - action: calculate_new_positions
    inputs: initial_positions, line_orientation, line_position, line_span
    rules:
      - condition: line_orientation == horizontal
        line_position: line_r
        line_span: [min_c, max_c]
        for_each: point (r, c) in initial_positions
        # Assuming points are below line (r > line_r). Adapt if points can be above.
        new_r: r - 5
        if: (c <= min_c) or (c >= max_c) # Outside or at ends of span
          new_c: c + 5
        else: # Strictly within span (min_c < c < max_c)
          new_c: c + 3
        output: (new_r, new_c)

      - condition: line_orientation == vertical
        line_position: line_c
        line_span: [min_r, max_r]
        for_each: point (r, c) in initial_positions
        # Assuming points are left of line (c < line_c). Adapt if points can be right.
        new_c: c + 4
        # No vertical movement observed in example
        new_r: r
        output: (new_r, new_c)
  - action: construct_output_grid
    inputs: input_grid_dimensions, static_line, moving_points_color, new_positions
    steps:
      - Create empty grid with background color (white).
      - Draw the static_line onto the grid.
      - Draw the moving_points_color at each calculated new_position.

assumptions:
  - Exactly one static line object exists.
  - Exactly one color identifies the moving points.
  - All moving points start on the same side relative to the line (e.g., all below, all left).
  - The movement magnitudes (e.g., 5 up, 3/5 right; 4 right, 0 up) are constant for this task.
  - The direction of movement components is consistent (e.g., always towards the line, secondary movement always right or always stationary vertically).
```


**Natural Language Program**

1.  Identify the single, continuous static line object (ignoring background color 0) and note its color, orientation (horizontal/vertical), position (row index or column index), and span (the range of columns or rows it covers).
2.  Identify all pixels that are not background and not part of the static line; these are the moving points. Note their color and initial positions.
3.  Create the output grid by copying the background and the static line object from the input grid.
4.  For each moving point found in step 2:
    a.  If the static line is **horizontal** (at row `line_r`, spanning columns `min_c` to `max_c`):
        i.  Calculate the new row by moving the point 5 steps vertically towards the line (new\_row = original\_row - 5, assuming points start below).
        ii. Calculate the new column based on the point's original column (`c`): If `c` is strictly between `min_c` and `max_c`, the new column is `c + 3`. Otherwise (if `c <= min_c` or `c >= max_c`), the new column is `c + 5`.
    b.  If the static line is **vertical** (at column `line_c`, spanning rows `min_r` to `max_r`):
        i.  Calculate the new column by moving the point 4 steps horizontally towards the line (new\_col = original\_col + 4, assuming points start to the left).
        ii. The new row is the same as the original row (new\_row = original\_row).
    c.  Place the moving point color at the calculated (new\_row, new\_col) position in the output grid.
5.  Return the completed output grid.
