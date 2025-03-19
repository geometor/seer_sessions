# a9f96cdd • 018 • refine_coder

---
```python
"""
1.  **Initialize Output:** Create an output grid of the same dimensions as the input grid, filled entirely with white pixels (value 0).
2.  **Locate All Red Pixels:** Find *all* red pixels (value 2) in the input grid and record their row and column indices.
3.  **Iterate Through Red Pixels:** For *each* red pixel found in the input grid:
    a. **Place Azure Pixel:** In the output grid, place an azure pixel (value 8) in the same row as the current red pixel, but one column to the *left*. If the red pixel is in the first column, wrap around and place the azure pixel in the last column.
    b. **Place Orange Pixel:** In the output grid, place an orange pixel (value 7) in the same row as the current red pixel, but one column to the *right*. If the red pixel is in the last column, wrap around and place the orange pixel in the first column.
4. **All other pixels:** Remain unchanged (0/white).
"""

import numpy as np

def find_all_red_pixels(grid):
    # Find the coordinates of all red pixels (value 2).
    rows, cols = np.where(grid == 2)
    return list(zip(rows, cols))

def transform(input_grid):
    # Initialize output grid of same dimension, filled with 0
    output_grid = np.zeros_like(input_grid)
    # Find all red pixels.
    red_pixel_coords_list = find_all_red_pixels(input_grid)

    rows, cols = input_grid.shape # Get dimensions for wraparound

    for row, col in red_pixel_coords_list:
        # Place the azure and orange pixels in output for each red pixel
        output_grid[row, (col - 1) % cols] = 8  # Left, wrap around
        output_grid[row, (col + 1) % cols] = 7  # Right, wrap around

    return output_grid
```
