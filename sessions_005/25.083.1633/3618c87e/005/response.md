```python
"""
1.  Identify Pixels: Locate all blue (1) and gray (5) pixels within the input grid.
2.  Move to Bottom: For *each* blue and gray pixel, perform the following:
    *   Determine the pixel's original column.
    *   Move the pixel to the bottom row of the output grid, placing it in the same column.
    *   If a blue pixel and a gray pixel occupy the same column, the blue pixel overwrites the gray pixel in the output.
3.  Clear Upper Rows:** Set all pixels in all rows *except* the bottom row to black (0).
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a given color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape
    bottom_row_index = rows - 1

    # Move blue (1) pixels to the bottom row
    blue_pixels = find_pixels_by_color(input_grid, 1)
    for r, c in blue_pixels:
        output_grid[bottom_row_index, c] = 1

    # Move gray (5) pixels to the bottom row, but blue will overwrite
    gray_pixels = find_pixels_by_color(input_grid, 5)
    for r, c in gray_pixels:
        # Only set to gray if the bottom row is not already blue
        if output_grid[bottom_row_index, c] != 1:
            output_grid[bottom_row_index, c] = 5

    return output_grid
```