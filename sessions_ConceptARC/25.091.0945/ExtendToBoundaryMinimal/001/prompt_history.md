
## train_1

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
4 4 4 4 4 4
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 4 0
```


**output:**
```
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
0 0 0 0 4 0
```


## train_3

**input:**
```
0 0 4 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
0 0 4 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
4 4 4 4 4 4
0 0 0 0 0 0
```

Okay, let's break down this task.

**Perception of the Elements:**

1.  **Grid Structure:** All examples use a 6x6 grid. The background color is consistently white (0).
2.  **Input Object:** Each input grid contains exactly one non-white pixel. This pixel is always yellow (4).
3.  **Transformation:** The transformation involves extending this single yellow pixel either horizontally across its entire row or vertically down its entire column.
4.  **Output Object:** The output grid retains the background color, but the single input pixel is replaced by a line (either a row or a column) of the same color (yellow).
5.  **Decision Logic:** The key seems to be determining *when* to extend horizontally (fill the row) versus vertically (fill the column). Observing the examples:
    *   If the yellow pixel is in the first column (column index 0), the entire row containing that pixel is filled yellow. (Examples 1 & 4)
    *   If the yellow pixel is *not* in the first column, the entire column containing that pixel is filled yellow. (Examples 2 & 3)

**YAML Facts:**


```yaml
task_context:
  grid_size: 6x6 (constant across examples)
  background_color: 0 (white)

input_elements:
  - object: marker_pixel
    properties:
      count: 1 per grid
      color: 4 (yellow)
      role: determines the line to be drawn in the output
    location: variable (row_index, column_index)

output_elements:
  - object: output_line
    properties:
      color: 4 (yellow) (same as input marker_pixel)
      orientation: determined by the input marker_pixel's location
      shape: horizontal row or vertical column spanning the grid

transformation_rule:
  - action: locate_marker_pixel
    inputs: input_grid
    outputs: marker_pixel_location (row_index, column_index), marker_pixel_color
  - action: determine_orientation
    based_on: marker_pixel_location.column_index
    condition:
      - if: column_index == 0
        then: orientation = horizontal (row)
      - else:
        then: orientation = vertical (column)
  - action: generate_output_grid
    properties:
      size: same as input grid
      initial_fill: background_color (0)
  - action: draw_line
    target: output_grid
    using: marker_pixel_color, marker_pixel_location, determined_orientation
    details:
      - if: orientation == horizontal
        then: fill row at marker_pixel_location.row_index with marker_pixel_color
      - if: orientation == vertical
        then: fill column at marker_pixel_location.column_index with marker_pixel_color
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid, but replace all non-white pixels with white (0).
2.  Scan the input grid to find the single non-white pixel. Record its color (C) and its position (row R, column Col).
3.  Check if the column index (Col) of the found pixel is 0.
4.  If Col is 0, fill the entire row R of the output grid with the color C.
5.  If Col is *not* 0, fill the entire column Col of the output grid with the color C.
6.  Return the modified output grid.
