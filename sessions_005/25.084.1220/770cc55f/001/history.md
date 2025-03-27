
## train_1

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


## train_4

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

Okay, let's break down this task.

### Perception

1.  **Input Structure:** The input grid always contains a single horizontal red line (color 2) separating the grid into an upper and lower section relative to the line. There is one contiguous block of a single color (blue, magenta, or green) in the top section and one contiguous block of the *same* color in the bottom section. The rest of the grid is white (color 0).
2.  **Output Structure:** The output grid is identical to the input grid, except for the addition of a rectangular block of yellow pixels (color 4).
3.  **Transformation:** The core transformation is the creation and placement of this yellow rectangle.
4.  **Yellow Rectangle Placement:**
    *   **Columns:** The yellow rectangle occupies the columns that are common to *both* the top colored block and the bottom colored block (their horizontal intersection).
    *   **Rows:** The yellow rectangle occupies the vertical space *either* between the top block and the red line *or* between the red line and the bottom block. It fills all the rows in the chosen space.
5.  **Determining Vertical Placement:** The decision of whether to place the yellow rectangle above or below the red line depends on how the intersection columns relate to the columns of the original top and bottom blocks:
    *   If the intersection columns exactly match the columns of the *bottom* block, the yellow rectangle is placed *above* the red line.
    *   If the intersection columns exactly match the columns of the *top* block, the yellow rectangle is placed *below* the red line.
    *   If the intersection columns are a proper subset of *both* the top block's columns and the bottom block's columns, the yellow rectangle is placed *above* the red line.

### Facts


```yaml
elements:
  - object: grid
    type: 2D array of integers (0-9)
  - object: red_line
    attributes:
      - color: 2 (red)
      - shape: horizontal line (1 pixel high)
      - location: spans the width of the grid at a specific row index
  - object: top_shape
    attributes:
      - color: variable (blue=1, magenta=6, or green=3)
      - shape: contiguous block
      - location: strictly above the red_line
  - object: bottom_shape
    attributes:
      - color: same as top_shape
      - shape: contiguous block
      - location: strictly below the red_line
  - object: background
    attributes:
      - color: 0 (white)
      - location: all cells not part of red_line, top_shape, or bottom_shape in the input

actions:
  - name: find_objects
    inputs: [grid]
    outputs: [red_line, top_shape, bottom_shape]
  - name: get_properties
    inputs: [red_line, top_shape, bottom_shape]
    outputs:
      - red_line_row: row index of red_line
      - top_shape_max_row: maximum row index of top_shape
      - bottom_shape_min_row: minimum row index of bottom_shape
      - top_shape_cols: set of column indices covered by top_shape
      - bottom_shape_cols: set of column indices covered by bottom_shape
  - name: calculate_intersection
    inputs: [top_shape_cols, bottom_shape_cols]
    outputs: [intersection_cols]
  - name: determine_fill_region
    inputs: [intersection_cols, top_shape_cols, bottom_shape_cols]
    outputs: [fill_above_red | fill_below_red]
    logic: |
      if intersection_cols == bottom_shape_cols:
        return fill_above_red
      elif intersection_cols == top_shape_cols:
        return fill_below_red
      else: # Assumes intersection is proper subset of both
        return fill_above_red
  - name: create_yellow_rectangle
    inputs: [grid_dimensions, fill_region_decision, red_line_row, top_shape_max_row, bottom_shape_min_row, intersection_cols]
    outputs: [yellow_pixels_coordinates]
    logic: |
      columns = intersection_cols
      if fill_region_decision == fill_above_red:
        rows = range(top_shape_max_row + 1, red_line_row)
      else: # fill_below_red
        rows = range(red_line_row + 1, bottom_shape_min_row)
      coordinates = set()
      for r in rows:
        for c in columns:
          coordinates.add((r, c))
      return coordinates
  - name: draw_output
    inputs: [input_grid, yellow_pixels_coordinates]
    outputs: [output_grid]
    logic: |
      Copy input_grid to output_grid.
      For each coordinate in yellow_pixels_coordinates:
        set output_grid[row][col] = 4 (yellow)

relationships:
  - type: spatial
    between: [top_shape, red_line, bottom_shape]
    description: top_shape is above red_line, bottom_shape is below red_line.
  - type: color
    between: [top_shape, bottom_shape]
    description: They always have the same color in the input.
  - type: dependency
    description: The location (columns and rows) of the new yellow rectangle depends on the locations (columns and rows) of the top_shape, bottom_shape, and red_line, and specifically on the relationship between their column sets.
```


### Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the horizontal red line (color 2). Store its row index (`red_row`).
3.  Identify the contiguous colored shape located entirely above the red line (`top_shape`). Determine the set of column indices it occupies (`top_cols`) and its maximum row index (`top_max_row`).
4.  Identify the contiguous colored shape located entirely below the red line (`bottom_shape`). Determine the set of column indices it occupies (`bottom_cols`) and its minimum row index (`bottom_min_row`).
5.  Calculate the set of column indices that are present in *both* `top_cols` and `bottom_cols` (the intersection: `intersection_cols`).
6.  Determine the vertical region to fill:
    *   If `intersection_cols` is identical to `bottom_cols`, the target region is Above the red line.
    *   If `intersection_cols` is identical to `top_cols`, the target region is Below the red line.
    *   Otherwise (if `intersection_cols` is a proper subset of both `top_cols` and `bottom_cols`), the target region is Above the red line.
7.  Define the rows to be filled based on the target region:
    *   If filling Above: The rows range from `top_max_row + 1` up to, but not including, `red_row`.
    *   If filling Below: The rows range from `red_row + 1` up to, but not including, `bottom_min_row`.
8.  Iterate through the determined `fill_rows` and the `intersection_cols`. For each combination `(row, col)`, set the corresponding pixel in the output grid to yellow (color 4).
9.  Return the modified output grid.
