# f5b8619d • 010 • refine_coder

---
```python
"""
1. Double Dimensions: Create an output grid with twice the height and twice the width of the input grid.
2. Iterate Input Pixels: For each pixel in the input grid:
    *   Get its color and its row (r) and column (c) coordinates.
    *   In the output grid, create a 2x2 block at the starting position (2*r, 2*c).
    *   Place the input pixel's color at the top-left corner of this block: `output_grid[2*r, 2*c] = input_pixel_color`.
    *   Fill the remaining three positions of the 2x2 block with azure (8):
        *   `output_grid[2*r + 1, 2*c] = 8`
        *   `output_grid[2*r, 2*c + 1] = 8`
        *   `output_grid[2*r + 1, 2*c + 1] = 8`
3. Return the output grid
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height, output_width = 2 * input_height, 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            input_pixel_color = input_grid[r, c]

            # Place the input pixel's color in the top-left of the 2x2 block
            output_grid[2*r, 2*c] = input_pixel_color

            # Fill the rest of the 2x2 block with azure (8)
            output_grid[2*r + 1, 2*c] = 8
            output_grid[2*r, 2*c + 1] = 8
            output_grid[2*r + 1, 2*c + 1] = 8

    return output_grid
```
