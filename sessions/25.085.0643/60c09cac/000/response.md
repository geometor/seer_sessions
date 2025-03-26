*   **Perception of the Elements:**
    *   The input grids contain a background color (white, 0) and a few pixels or small groups of pixels of other colors (azure, gray, green, orange).
    *   The output grids are larger than the input grids. Specifically, the output grids appear to be exactly twice the height and twice the width of the corresponding input grids.
    *   Each pixel in the input grid seems to correspond to a 2x2 block of pixels of the same color in the output grid.
    *   The relative positions of the colored blocks in the output grid correspond to the relative positions of the colored pixels in the input grid, but scaled up.
    *   The background color (white) also expands into 2x2 blocks.

*   **YAML Facts:**


```yaml
task_description: Scale the input grid by a factor of 2 in both height and width.
elements:
  - type: grid
    properties:
      - input_grid: H x W dimensions
      - output_grid: (H*2) x (W*2) dimensions
  - type: pixel
    properties:
      - color: Any integer from 0-9
      - position: (row, column) coordinates in the grid
transformation:
  - action: scale
    details: Each pixel in the input grid is replaced by a 2x2 block of the same color in the output grid.
  - mapping:
    input_pixel_at: (r, c) with color C
    output_block_top_left_at: (r*2, c*2) with size 2x2 and color C
relationship:
  - The output grid dimensions are double the input grid dimensions.
  - The position of the top-left corner of the 2x2 output block is determined by doubling the row and column indices of the corresponding input pixel.
```


*   **Natural Language Program:**

1.  Determine the dimensions (height H, width W) of the input grid.
2.  Create a new output grid with dimensions (H * 2) by (W * 2), initially filled with a default color (e.g., white/0, although the process overwrites everything).
3.  Iterate through each pixel in the input grid at position (row `r`, column `c`) from `r = 0` to `H-1` and `c = 0` to `W-1`.
4.  For each input pixel at (`r`, `c`), get its color `C`.
5.  In the output grid, fill a 2x2 block of pixels with the color `C`. The top-left corner of this block will be at position (`r * 2`, `c * 2`). Specifically, the pixels at (`r * 2`, `c * 2`), (`r * 2 + 1`, `c * 2`), (`r * 2`, `c * 2 + 1`), and (`r * 2 + 1`, `c * 2 + 1`) in the output grid should all be set to color `C`.
6.  Return the completed output grid.