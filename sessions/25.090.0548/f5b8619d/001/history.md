
## train_1

**input:**
```
0 5 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
5 0 0 0 0 5
0 0 0 0 0 0
```


**output:**
```
8 5 0 0 0 8 8 5 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
5 8 0 0 0 5 5 8 0 0 0 5
8 8 0 0 0 8 8 8 0 0 0 8
8 5 0 0 0 8 8 5 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
8 8 0 0 0 8 8 8 0 0 0 8
5 8 0 0 0 5 5 8 0 0 0 5
8 8 0 0 0 8 8 8 0 0 0 8
```


## train_2

**input:**
```
2 0 0
0 0 0
0 0 2
```


**output:**
```
2 0 8 2 0 8
8 0 8 8 0 8
8 0 2 8 0 2
2 0 8 2 0 8
8 0 8 8 0 8
8 0 2 8 0 2
```


## train_3

**input:**
```
0 4
0 0
```


**output:**
```
0 4 0 4
0 8 0 8
0 4 0 4
0 8 0 8
```

**Perception of the Elements:**

1.  **Grid Size:** The output grid is always twice the height and twice the width of the input grid.
2.  **Structure:** The output grid appears to be constructed by taking a modified version of the input grid (let's call it the "base tile") and tiling it 2x2.
3.  **Color Preservation:** Non-white pixels (gray 5, red 2, yellow 4 in the examples) from the input grid seem to keep their original color and relative position within the base tile.
4.  **Color Transformation:** Some white (0) pixels in the input grid are transformed into azure (8) pixels in the base tile. Other white pixels remain white.
5.  **Transformation Rule:** The transformation of white pixels to azure seems dependent on their position relative to the non-white pixels in the *original* input grid. A white pixel at position (r, c) becomes azure (8) if *either* row 'r' *or* column 'c' of the input grid contains at least one non-white pixel. If both the row and column containing the white pixel are entirely white in the input, the pixel remains white (0) in the base tile.
6.  **Tiling:** Once the base tile is generated according to rules 3-5, the final output is created by repeating this base tile in a 2x2 arrangement.

**YAML Facts:**


```yaml
task_context:
  grid_transformation: true
  output_grid_properties:
    size_relation: Double height and double width compared to the input grid.
    structure: 2x2 tiling of a derived 'base_tile'.
base_tile_derivation:
  source: Input grid.
  dimensions: Same as input grid.
  pixel_mapping:
    - condition: Input pixel is non-white.
      action: Copy the input pixel's color to the corresponding position in the base_tile.
    - condition: Input pixel is white (0).
      action:
        - check: Does the input grid's row containing this pixel OR the input grid's column containing this pixel have any non-white pixels?
        - result_true: Set the corresponding base_tile pixel to azure (8).
        - result_false: Keep the corresponding base_tile pixel as white (0).
final_output_construction:
  method: Tiling.
  pattern: Repeat the derived base_tile grid 2 times horizontally and 2 times vertically.
  result_dimensions: 2 * input_height x 2 * input_width.
identified_objects:
  - background: White pixels (0).
  - foreground: Non-white pixels (variable colors). Their position dictates the transformation.
  - derived: Azure pixels (8), created based on the position of foreground pixels.
relationships:
  - Row/Column Containment: The key relationship is whether a given row or column in the input contains any non-white pixels. This determines the fate of white pixels in that row/column during the base tile creation.
```


**Natural Language Program:**

1.  Receive the input grid. Determine its height (H) and width (W).
2.  Create a new intermediate grid, `base_tile`, of the same dimensions (H x W).
3.  Find all rows in the input grid that contain at least one non-white pixel. Store their indices in a set called `rows_with_non_white`.
4.  Find all columns in the input grid that contain at least one non-white pixel. Store their indices in a set called `cols_with_non_white`.
5.  Iterate through each cell of the input grid at row `r` (from 0 to H-1) and column `c` (from 0 to W-1):
    a.  Let `input_color` be the color of the input grid cell at (r, c).
    b.  If `input_color` is not white (0), set the cell `base_tile[r, c]` to `input_color`.
    c.  If `input_color` is white (0):
        i.  Check if `r` is in `rows_with_non_white` OR if `c` is in `cols_with_non_white`.
        ii. If the check is true, set `base_tile[r, c]` to azure (8).
        iii. If the check is false, set `base_tile[r, c]` to white (0).
6.  Create the final output grid with dimensions (2*H) x (2*W).
7.  Place copies of the `base_tile` into the four quadrants of the output grid:
    *   Top-left quadrant (rows 0 to H-1, columns 0 to W-1): Copy `base_tile`.
    *   Top-right quadrant (rows 0 to H-1, columns W to 2*W-1): Copy `base_tile`.
    *   Bottom-left quadrant (rows H to 2*H-1, columns 0 to W-1): Copy `base_tile`.
    *   Bottom-right quadrant (rows H to 2*H-1, columns W to 2*W-1): Copy `base_tile`.
8.  Return the completed output grid.
