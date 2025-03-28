
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 3 2 2 2 3 0 0 0 0 8
0 3 2 2 2 3 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3
0 3 2 2 2 2 2 2 2 2 3
0 3 2 2 2 2 2 2 2 2 3
0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 1 1 2 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 1 6 1 0 0 0 0 0 0 0
0 0 1 6 1 0 0 0 0 0 0 0
0 0 1 6 1 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 1 0
0 0 1 6 6 6 6 6 6 6 1 0
0 0 1 6 6 6 6 6 6 6 1 0
0 0 1 6 6 6 6 6 6 6 1 0
0 0 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Input Grids:** Each input grid contains a background of white pixels (0). There is a primary "shape" composed of non-white pixels. This shape can be a simple rectangle or a rectangle containing an inner pattern/color. Crucially, each input grid also contains a single, isolated azure pixel (8) located somewhere outside the primary shape.
2.  **Output Grids:** The output grids show a modified version of the primary shape from the input. The shape has been extended either horizontally to the right or vertically downwards. The azure pixel is no longer present in the output grid; it seems to act as an instruction rather than part of the final image.
3.  **Transformation:** The transformation involves stretching or extending the primary shape. The direction and extent of this extension appear to be dictated by the position of the azure pixel relative to the original shape.
    *   If the azure pixel is located to the right of the shape's rightmost boundary, the shape extends horizontally to the right.
    *   If the azure pixel is located below the shape's bottommost boundary, the shape extends vertically downwards.
    *   The extension fills the space between the original boundary of the shape and the coordinate (column or row) indicated by the azure pixel.
    *   The pixels used for the extension are copies of the pixels found on the edge of the shape that is being extended. For a rightward extension, the rightmost column of the shape is duplicated. For a downward extension, the bottommost row of the shape is duplicated.

**YAML Facts:**


```yaml
task_description: Extend a shape based on the position of a marker pixel.

elements:
  - role: background
    color: white (0)
    description: The base color of the grid.
  - role: shape
    color: any non-white, non-azure color (e.g., green, red, blue, magenta)
    description: A contiguous object or pattern, often rectangular, that is the main subject of the transformation. Can contain internal patterns.
    properties:
      - bounding_box: Defines the min/max row and column indices.
  - role: marker
    color: azure (8)
    description: A single, isolated pixel indicating the direction and extent of the transformation.
    properties:
      - position: Row and column index (r, c).
      - relative_position: Position relative to the shape's bounding box (e.g., right of, below).

actions:
  - name: identify_shape_bounds
    input: input_grid
    output: min_row, max_row, min_col, max_col for non-white, non-azure pixels.
  - name: identify_marker_position
    input: input_grid
    output: marker_row, marker_col for the azure pixel.
  - name: determine_extension_direction
    input: shape_bounds, marker_position
    output: direction ('right' or 'down')
    logic: If marker_col > max_col, direction is 'right'. If marker_row > max_row, direction is 'down'. (Based on examples, assuming only these two directions).
  - name: determine_extension_boundary
    input: marker_position, direction
    output: boundary_index (target column or row)
    logic: If direction is 'right', boundary_index is marker_col. If direction is 'down', boundary_index is marker_row.
  - name: extract_edge_pattern
    input: input_grid, shape_bounds, direction
    output: edge_pixel_pattern (a row or column of pixels)
    logic: If direction is 'right', extract the column at max_col within shape's row bounds. If direction is 'down', extract the row at max_row within shape's column bounds.
  - name: apply_extension
    input: input_grid, shape_bounds, direction, boundary_index, edge_pattern
    output: output_grid
    logic: Create a copy of the input grid. If direction is 'right', copy the edge_pattern (column) into columns from max_col + 1 to boundary_index, within the shape's original row bounds. If direction is 'down', copy the edge_pattern (row) into rows from max_row + 1 to boundary_index, within the shape's original column bounds. Set the original marker pixel position to white (0).

relationships:
  - The marker's position relative to the shape determines the extension direction.
  - The marker's column index determines the new right boundary for rightward extension.
  - The marker's row index determines the new bottom boundary for downward extension.
  - The pixels on the edge of the original shape are used as the pattern for the extension.

output_grid_properties:
  - Contains the extended shape.
  - Does not contain the azure marker pixel.
  - Background remains white.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Locate the single azure (8) pixel in the input grid and record its row (`marker_row`) and column (`marker_col`). Set the pixel at (`marker_row`, `marker_col`) in the output grid to white (0).
3.  Identify the bounding box of the primary shape(s) in the input grid by finding the minimum and maximum row and column indices (`min_row`, `max_row`, `min_col`, `max_col`) occupied by non-white (0) and non-azure (8) pixels.
4.  Compare the marker's position to the shape's bounding box:
    *   If `marker_col` is greater than `max_col`:
        *   Set the extension direction to 'right'.
        *   The target boundary column (`target_col`) is `marker_col`.
        *   Extract the column of pixels from the input grid at `max_col`, for rows from `min_row` to `max_row`. This is the `edge_pattern`.
        *   For each column `c` from `max_col + 1` up to (but not including) `target_col`:
            *   For each row `r` from `min_row` to `max_row`:
                *   Set the pixel in the output grid at (`r`, `c`) to the color found at (`r`, `max_col`) in the input grid (i.e., copy the `edge_pattern`).
    *   Else if `marker_row` is greater than `max_row`:
        *   Set the extension direction to 'down'.
        *   The target boundary row (`target_row`) is `marker_row`.
        *   Extract the row of pixels from the input grid at `max_row`, for columns from `min_col` to `max_col`. This is the `edge_pattern`.
        *   For each row `r` from `max_row + 1` up to (but not including) `target_row`:
            *   For each column `c` from `min_col` to `max_col`:
                *   Set the pixel in the output grid at (`r`, `c`) to the color found at (`max_row`, `c`) in the input grid (i.e., copy the `edge_pattern`).
5.  Return the modified output grid.
