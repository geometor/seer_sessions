
## train_1

**input:**
```
2 7 3 5 0 0 0 0 0 0 0 0 0
2 3 3 5 0 0 0 0 1 0 0 0 0
3 7 7 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 1 0 0 0 0 0 1 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 1 0 0 1 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 7 3 5 0 0 0 2 7 3 0 0 0
2 3 3 5 0 0 0 2 3 3 0 0 0
3 7 7 5 0 0 0 3 7 7 0 0 0
0 0 0 5 2 7 3 0 0 0 2 7 3
0 0 0 5 2 3 3 0 0 0 2 3 3
0 0 0 5 3 7 7 0 0 0 3 7 7
0 0 0 5 2 7 3 2 7 3 0 0 0
0 0 0 5 2 3 3 2 3 3 0 0 0
0 0 0 5 3 7 7 3 7 7 0 0 0
```


## train_2

**input:**
```
4 2 2 5 0 0 0 0 0 0 0 0 0
2 6 2 5 0 1 0 0 0 0 0 0 0
6 4 4 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 1 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 1 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 2 2 5 4 2 2 0 0 0 0 0 0
2 6 2 5 2 6 2 0 0 0 0 0 0
6 4 4 5 6 4 4 0 0 0 0 0 0
0 0 0 5 0 0 0 4 2 2 0 0 0
0 0 0 5 0 0 0 2 6 2 0 0 0
0 0 0 5 0 0 0 6 4 4 0 0 0
0 0 0 5 0 0 0 4 2 2 0 0 0
0 0 0 5 0 0 0 2 6 2 0 0 0
0 0 0 5 0 0 0 6 4 4 0 0 0
```


## train_3

**input:**
```
3 8 6 5 0 0 0 0 0 0 0 0 0
9 8 2 5 0 1 0 0 0 0 0 1 0
9 9 9 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 1 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 1 0 0 1 0
0 0 0 5 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 8 6 5 3 8 6 0 0 0 3 8 6
9 8 2 5 9 8 2 0 0 0 9 8 2
9 9 9 5 9 9 9 0 0 0 9 9 9
0 0 0 5 0 0 0 3 8 6 0 0 0
0 0 0 5 0 0 0 9 8 2 0 0 0
0 0 0 5 0 0 0 9 9 9 0 0 0
0 0 0 5 0 0 0 3 8 6 3 8 6
0 0 0 5 0 0 0 9 8 2 9 8 2
0 0 0 5 0 0 0 9 9 9 9 9 9
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Grid Structure:** Both input and output grids have the same dimensions (9 rows x 13 columns in the examples).
2.  **Persistent Elements:**
    *   A 3x3 pattern of various colors always exists in the top-left corner (rows 0-2, columns 0-2). Let's call this the "source pattern".
    *   A vertical line of gray pixels (color 5) consistently appears in the 4th column (index 3).
3.  **Variable Elements (Input):**
    *   Blue pixels (color 1) appear sporadically in the area to the right of the gray line. Their positions vary between examples.
4.  **Transformation:**
    *   The output grid largely resembles the input grid initially.
    *   The key change is that wherever a blue pixel (1) existed in the input, a copy of the "source pattern" is placed in the output grid.
    *   The top-left corner of the copied pattern corresponds exactly to the location of the original blue pixel.
    *   The blue pixels themselves are *replaced* by the top-left pixel of the copied source pattern.
    *   If placing the 3x3 source pattern extends beyond the grid boundaries (specifically, the right edge in these examples), the pattern is clipped; only the parts that fit within the grid are drawn.
    *   The original source pattern in the top-left and the gray line remain unchanged in the output.

**YAML Facts:**


```yaml
task_context:
  grid_dimensions:
    - input_shape: [9, 13] # based on examples
    - output_shape: [9, 13] # same as input
  persistent_elements:
    - object: source_pattern
      description: A 3x3 subgrid of non-white pixels.
      location: Top-left corner (rows 0-2, cols 0-2).
      role: Template to be copied.
    - object: vertical_divider
      description: A vertical line of pixels.
      color: gray (5)
      location: Column index 3.
      role: Static background element, separates source pattern area from target area.
  variable_elements:
    - object: marker_pixels
      description: Individual pixels indicating target locations.
      color: blue (1)
      location: Variable coordinates (row, col), always to the right of the vertical_divider (col > 3).
      role: Trigger points for pattern placement.
transformation:
  action: copy_paste_pattern
  source_object: source_pattern
  target_locations: Determined by the coordinates of marker_pixels.
  placement_rule: The top-left corner of the source_pattern is placed at the exact coordinates of each marker_pixel.
  modification: The marker_pixels are replaced/overwritten during the paste operation.
  boundary_handling: If the pasted pattern exceeds grid boundaries, it is clipped.
  result: Output grid contains the original persistent elements plus copies of the source_pattern placed at marker_pixel locations.
```


**Natural Language Program:**

1.  Initialize the `output_grid` as an identical copy of the `input_grid`.
2.  Identify the 3x3 `source_pattern` by extracting the subgrid from the `input_grid` at rows 0-2 and columns 0-2.
3.  Find the coordinates `(r, c)` of all pixels in the `input_grid` that have the color blue (1).
4.  For each blue pixel coordinate `(r_target, c_target)` found:
    a.  Iterate through the `source_pattern` using relative row index `dr` (from 0 to 2) and relative column index `dc` (from 0 to 2).
    b.  Calculate the corresponding destination coordinates in the `output_grid`: `r_out = r_target + dr`, `c_out = c_target + dc`.
    c.  Check if `r_out` and `c_out` are within the valid row and column bounds of the `output_grid`.
    d.  If the coordinates `(r_out, c_out)` are within bounds, update the pixel at `output_grid[r_out, c_out]` with the value from `source_pattern[dr, dc]`.
5.  Return the modified `output_grid`.
