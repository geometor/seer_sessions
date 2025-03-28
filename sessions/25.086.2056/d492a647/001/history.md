
## train_1

**input:**
```
0 0 5 0 5 5 5 0 5 0 5 5 5
5 5 0 5 0 0 5 5 0 5 5 5 5
5 0 5 0 0 0 0 0 0 0 0 0 0
5 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 0 0 1 0 0 0 0 0 5 5
0 5 5 0 0 0 0 0 0 0 0 5 5
0 5 5 0 0 0 0 0 0 0 0 0 5
5 0 5 0 0 0 0 0 0 0 0 0 5
5 5 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 5 5
0 0 5 5 0 5 0 5 0 5 5 5 5
5 5 5 0 5 5 5 5 5 5 5 5 5
5 5 0 5 0 5 5 5 5 0 5 0 5
```


**output:**
```
0 1 5 1 5 5 5 1 5 1 5 5 5
5 5 0 5 0 0 5 5 0 5 5 5 5
5 1 5 1 0 1 0 1 0 1 0 1 0
5 0 0 0 0 0 0 0 0 0 0 0 0
5 5 5 1 0 1 0 1 0 1 0 5 5
0 5 5 0 0 0 0 0 0 0 0 5 5
0 5 5 1 0 1 0 1 0 1 0 1 5
5 0 5 0 0 0 0 0 0 0 0 0 5
5 5 5 1 0 1 0 1 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0 0 5 5
0 1 5 5 0 5 0 5 0 5 5 5 5
5 5 5 0 5 5 5 5 5 5 5 5 5
5 5 0 5 0 5 5 5 5 1 5 1 5
```


## train_2

**input:**
```
5 0 5 0 5 5 5 5 5 5 5 0 5 0 5 5
0 5 5 0 5 5 5 0 5 0 0 5 0 0 5 5
5 5 5 0 0 0 0 0 0 0 0 0 0 5 5 0
5 5 0 0 0 0 0 0 0 0 0 5 0 5 5 0
5 0 5 0 0 0 0 0 0 0 0 5 5 5 0 0
5 5 5 0 0 0 0 3 0 0 0 0 0 5 0 0
0 5 0 0 0 0 0 0 0 0 0 5 5 0 5 0
0 5 5 0 0 0 0 0 0 0 0 0 5 5 5 5
0 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5
0 5 5 5 0 5 5 5 5 5 0 5 0 5 0 0
5 5 5 5 0 5 0 5 0 0 0 5 0 5 0 0
0 5 5 0 0 5 0 5 0 0 0 0 5 5 0 5
5 5 0 5 5 5 5 5 5 0 5 5 5 5 0 5
```


**output:**
```
5 0 5 0 5 5 5 5 5 5 5 0 5 0 5 5
0 5 5 3 5 5 5 3 5 3 0 5 0 3 5 5
5 5 5 0 0 0 0 0 0 0 0 0 0 5 5 0
5 5 0 3 0 3 0 3 0 3 0 5 0 5 5 3
5 0 5 0 0 0 0 0 0 0 0 5 5 5 0 0
5 5 5 3 0 3 0 3 0 3 0 3 0 5 0 3
0 5 0 0 0 0 0 0 0 0 0 5 5 0 5 0
0 5 5 3 0 3 0 3 0 3 0 3 5 5 5 5
0 5 0 0 0 0 0 0 0 0 0 5 5 5 5 5
0 5 5 5 0 5 5 5 5 5 0 5 0 5 0 3
5 5 5 5 0 5 0 5 0 0 0 5 0 5 0 0
0 5 5 3 0 5 0 5 0 3 0 3 5 5 0 5
5 5 0 5 5 5 5 5 5 0 5 5 5 5 0 5
```

**Perception**

1.  **Grid Structure:** Both input and output grids are 2D arrays of pixels represented by integer color codes. The grid dimensions remain unchanged between input and output for each example (13x13 for train_1, 13x16 for train_2).
2.  **Color Palette:** The primary colors involved are white (0) and gray (5). Each input example features exactly one pixel of a distinct color (blue=1 in train_1, green=3 in train_2). The output grids contain the same set of colors as their corresponding inputs.
3.  **Transformation Core:** The key transformation involves changing some white (0) pixels to the unique color present in the input (blue or green). Gray (5) pixels and the original unique colored pixel remain unchanged.
4.  **Pattern Identification:** The locations where white pixels are changed follow a grid-like pattern based on the parity (even/odd) of the row and column indices. This parity pattern seems directly linked to the parity of the row and column indices of the unique colored pixel in the input grid.
5.  **Rule Hypothesis:** The transformation identifies the unique non-white, non-gray pixel (let's call it the 'target pixel' with 'target color'). It determines the parity (even/odd) of the target pixel's row and column coordinates. Then, it iterates through the grid, changing any white (0) pixel to the 'target color' *if and only if* its row parity matches the target pixel's row parity AND its column parity matches the target pixel's column parity. All other pixels retain their original color.

**Facts**


```yaml
task_type: color_transformation
grid_properties:
  - dimensions_preserved: True
  - background_color: white (0)
  - static_color: gray (5) # Pixels that generally do not change
objects:
  - object_type: target_pixel
    description: A single pixel in the input grid whose color is neither white (0) nor gray (5).
    properties:
      - color: Varies per example (e.g., blue=1, green=3). Let's call this 'target_color'.
      - position: (row, column) coordinates within the grid. Let's call this ('target_row', 'target_col').
      - count: Exactly one per input grid.
    role: Determines the color and location pattern for the transformation.
  - object_type: background_pixels
    description: Pixels with the background color (white=0).
    properties:
      - color: white (0)
      - position: (row, column) coordinates.
    role: Some of these pixels are targets for color change.
relationships:
  - relation: parity_matching
    description: >
      The transformation depends on matching the parity (even/odd) of a white pixel's
      row and column indices with the parity of the target_pixel's row and column indices.
    condition: Applies only to white (0) pixels.
    source: target_pixel (its row/col parity)
    target: background_pixels (white=0)
actions:
  - action: find_target_pixel
    description: Locate the unique pixel in the input grid that is not white (0) or gray (5). Record its color ('target_color') and position ('target_row', 'target_col').
  - action: determine_parity_rule
    description: >
      Determine the required parity for rows (even/odd based on 'target_row') and
      columns (even/odd based on 'target_col').
  - action: apply_color_change
    description: >
      Iterate through each pixel of the input grid. If a pixel is white (0) AND
      its row index parity matches the target row parity AND its column index parity
      matches the target column parity, change its color to 'target_color' in the
      output grid. Otherwise, copy the input pixel's color to the output grid.
```


**Natural Language Program**

1.  Initialize the output grid as an exact copy of the input grid.
2.  Scan the input grid to find the single pixel whose color is not white (0) and not gray (5). Store this pixel's color as `target_color` and its coordinates as (`target_row`, `target_col`).
3.  Determine the parity of `target_row` (is it even or odd?). Store this as `required_row_parity`.
4.  Determine the parity of `target_col` (is it even or odd?). Store this as `required_col_parity`.
5.  Iterate through each cell (`r`, `c`) of the input grid:
    a.  Check if the color of the input cell at (`r`, `c`) is white (0).
    b.  Check if the parity of the current row index `r` matches `required_row_parity`.
    c.  Check if the parity of the current column index `c` matches `required_col_parity`.
    d.  If all three conditions (5a, 5b, 5c) are true, update the cell at (`r`, `c`) in the *output grid* to `target_color`.
6.  Return the modified output grid.
