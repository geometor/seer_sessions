
## train_1

**input:**
```
0 3 3 3
0 0 0 0
0 0 0 0
0 0 0 0
2 2 2 2
0 0 0 0
0 0 0 0
0 0 0 0
3 3 0 0
```


**output:**
```
0 3 3 3
0 4 0 0
0 4 0 0
0 4 0 0
2 2 2 2
0 0 0 0
0 0 0 0
0 0 0 0
3 3 0 0
```


## train_2

**input:**
```
0 6 6 6 6
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 6 6 6
```


**output:**
```
0 6 6 6 6
0 0 4 4 4
0 0 4 4 4
0 0 4 4 4
0 0 4 4 4
0 0 4 4 4
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 6 6 6
```


## train_3

**input:**
```
0 1 1 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
1 1 1 1 0
```


**output:**
```
0 1 1 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
2 2 2 2 2
0 4 4 0 0
0 4 4 0 0
0 4 4 0 0
0 4 4 0 0
0 4 4 0 0
1 1 1 1 0
```


## train_4

**input:**
```
0 0 0 3 3 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 3 3 3 3 3
```


**output:**
```
0 0 0 3 3 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 4 4 0
0 0 0 4 4 0
0 0 0 4 4 0
0 0 0 4 4 0
0 0 0 4 4 0
0 3 3 3 3 3
```

## Perception

The task involves modifying an input grid based on the relative positions and sizes of three horizontal line segments.
1.  **Input Structure:** Each input grid contains exactly one horizontal red line, one non-red/non-white horizontal line segment positioned above the red line (the "top line"), and one non-red/non-white horizontal line segment positioned below the red line (the "bottom line"). The rest of the grid is typically white (color 0).
2.  **Output Structure:** The output grid preserves the original red, top, and bottom lines and the white background. The only change is the addition of a rectangular area filled with yellow pixels (color 4).
3.  **Transformation:** The key is determining the location and dimensions of the yellow rectangle.
    *   **Columns:** The columns occupied by the yellow rectangle are precisely those columns where the top line and the bottom line overlap horizontally (their intersection).
    *   **Rows:** The rows occupied by the yellow rectangle depend on a comparison of the widths (number of columns) of the top and bottom lines:
        *   If the bottom line is strictly narrower than the top line, the yellow rectangle fills the rows strictly *between* the top line and the red line.
        *   Otherwise (if the top line is narrower than or equal in width to the bottom line), the yellow rectangle fills the rows strictly *between* the red line and the bottom line.

## Facts


```yaml
objects:
  - type: grid
    properties:
      - background_color: white (0)
  - type: line_segment
    identifier: top_line
    properties:
      - color: non-red (2), non-white (0) # e.g., green(3), magenta(6), blue(1)
      - orientation: horizontal
      - position: located in a single row above the red_line
      - row_index: integer
      - column_indices: set of integers
      - width: integer (count of column_indices)
  - type: line_segment
    identifier: bottom_line
    properties:
      - color: non-red (2), non-white (0) # e.g., green(3), magenta(6), blue(1)
      - orientation: horizontal
      - position: located in a single row below the red_line
      - row_index: integer
      - column_indices: set of integers
      - width: integer (count of column_indices)
  - type: line_segment
    identifier: red_line
    properties:
      - color: red (2)
      - orientation: horizontal
      - position: located in a single row between top_line and bottom_line
      - row_index: integer
  - type: rectangle
    identifier: yellow_fill
    properties:
      - color: yellow (4)
      - position: derived from other objects
      - row_indices: set of integers
      - column_indices: set of integers

relationships_and_actions:
  - action: identify
    actor: system
    target: top_line, bottom_line, red_line
    details: Locate these three line segments in the input grid based on color and relative vertical position. Record their row indices, column indices, and widths.
  - action: calculate_intersection
    actor: system
    inputs: top_line.column_indices, bottom_line.column_indices
    output: yellow_fill.column_indices
    details: Find the common column indices shared by the top_line and bottom_line.
  - action: determine_rows
    actor: system
    inputs: top_line.width, bottom_line.width, top_line.row_index, red_line.row_index, bottom_line.row_index
    output: yellow_fill.row_indices
    condition:
      - if: bottom_line.width < top_line.width
        then: yellow_fill.row_indices are all integers strictly between top_line.row_index and red_line.row_index.
      - else: # (top_line.width <= bottom_line.width)
        then: yellow_fill.row_indices are all integers strictly between red_line.row_index and bottom_line.row_index.
  - action: create_output
    actor: system
    inputs: input_grid, yellow_fill.row_indices, yellow_fill.column_indices
    details: Start with a copy of the input grid. For every row index in yellow_fill.row_indices and every column index in yellow_fill.column_indices, set the corresponding pixel to yellow (4).
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to find the horizontal red line (color 2). Record its row index (`red_row`).
3.  Scan the input grid to find the highest non-red, non-white horizontal line segment above the `red_row`. Record its row index (`top_row`), its set of column indices (`top_cols`), and its width (`top_width`, which is the count of `top_cols`).
4.  Scan the input grid to find the lowest non-red, non-white horizontal line segment below the `red_row`. Record its row index (`bottom_row`), its set of column indices (`bottom_cols`), and its width (`bottom_width`, which is the count of `bottom_cols`).
5.  Calculate the set of column indices that are present in both `top_cols` and `bottom_cols`. This is the intersection (`intersection_cols`).
6.  Compare the widths:
    *   If `bottom_width` is less than `top_width`: Define the target rows (`target_rows`) as all row indices strictly between `top_row` and `red_row`.
    *   Otherwise (if `top_width` is less than or equal to `bottom_width`): Define the target rows (`target_rows`) as all row indices strictly between `red_row` and `bottom_row`.
7.  Iterate through each row index `r` in `target_rows` and each column index `c` in `intersection_cols`.
8.  Set the pixel at position (`r`, `c`) in the output grid to yellow (color 4).
9.  Return the modified output grid.
