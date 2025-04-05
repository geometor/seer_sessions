
## train_1

**input:**
```
0 2 0 0 0
2 2 2 0 0
0 2 0 0 0
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 2 0 0
0 2 2 2 0
0 0 2 0 0
0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 5
0 0 0 0 5
0 0 5 5 5
0 0 0 0 0
0 0 0 0 0
```


**output:**
```
0 0 0 0 0
0 0 0 5 0
0 0 0 5 0
0 5 5 5 0
0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0
0 0 0 0 0
6 6 6 0 0
6 0 6 0 0
6 0 6 0 0
```


**output:**
```
0 0 0 0 0
0 6 6 6 0
0 6 0 6 0
0 6 0 6 0
0 0 0 0 0
```

Okay, analyzing the provided examples.

**Perception:**

The task involves transforming a 2D grid of numbers. Each input grid contains a single "shape" composed of identical non-zero numbers against a background of zeros. The output grid shows the same shape, using the same non-zero number, but moved to a different position. The shape itself (relative positions of its constituent cells) remains unchanged. The movement appears to center the shape within the grid. Specifically, the center of the shape's bounding box in the input is moved to the center of the grid in the output.

**YAML Facts:**


```yaml
task_elements:
  - object: grid
    properties:
      - type: 2D array of integers
      - dimensions: 5x5 (in examples)
      - background_value: 0
  - object: shape
    properties:
      - defined_by: non-zero cells in the input grid
      - color: the specific non-zero integer value
      - structure: relative positions of non-zero cells
    relationships:
      - contained_within: input grid
  - object: bounding_box
    properties:
      - defined_by: min/max row and column indices of the shape
      - center: calculated from min/max indices (floor average)
    relationships:
      - encloses: shape
  - object: grid_center
    properties:
      - coordinates: (floor(height/2), floor(width/2))
      - value: (2, 2) for a 5x5 grid
  - action: identify_shape
    inputs: input_grid
    outputs: shape_cells, shape_color
  - action: calculate_bounding_box
    inputs: shape_cells
    outputs: min_row, max_row, min_col, max_col
  - action: calculate_center
    inputs: min_row, max_row, min_col, max_col
    outputs: center_coordinates (row, col)
  - action: calculate_shift
    inputs: bounding_box_center, grid_center
    outputs: shift_vector (delta_row, delta_col)
  - action: apply_shift
    inputs: shape_cells, shape_color, shift_vector, grid_dimensions
    outputs: output_grid
```


**Natural Language Program:**

1.  **Initialize:** Create an output grid with the same dimensions as the input grid, filled entirely with the background value (0).
2.  **Identify Shape:** Locate all cells in the input grid containing a non-zero value. Store their coordinates and the common non-zero value (the shape's "color"). If no non-zero cells exist, return the initialized output grid.
3.  **Find Bounding Box:** Determine the minimum row, maximum row, minimum column, and maximum column indices occupied by the identified shape cells.
4.  **Calculate Input Center:** Compute the center coordinates (row, col) of the shape's bounding box using integer division or floor: `center_row = floor((min_row + max_row) / 2)`, `center_col = floor((min_col + max_col) / 2)`.
5.  **Determine Grid Center:** Identify the center coordinates (row, col) of the grid itself: `grid_center_row = floor(grid_height / 2)`, `grid_center_col = floor(grid_width / 2)`. For the 5x5 examples, this is (2, 2).
6.  **Calculate Shift:** Calculate the displacement vector (delta_row, delta_col) needed to move the shape's bounding box center to the grid center: `delta_row = grid_center_row - center_row`, `delta_col = grid_center_col - center_col`.
7.  **Translate Shape:** For each non-zero cell (r, c) identified in step 2:
    a. Calculate its new position (new_r, new_c) by adding the shift vector: `new_r = r + delta_row`, `new_c = c + delta_col`.
    b. Place the shape's color (the non-zero value) into the output grid at coordinates (new_r, new_c).
8.  **Return Output:** Return the modified output grid containing the translated shape.
