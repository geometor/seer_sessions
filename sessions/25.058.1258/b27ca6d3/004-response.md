# b27ca6d3 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** all red (2) pixels in the input grid.
2.  **For each** red (2) pixel:
    *   **Check** the directly adjacent pixels (up, down, left, and right - not diagonal).
    * Specifically find the group of 3 pixels: the top, middle, and bottom of the row, or the left, middle, and right of the column.
    * If a horizontal or vertical group of three such cells all exist, **change** the color of adjacent white (0) pixels to green (3) *within that set of 3*.
3.  **Leave** all other pixels unchanged.
4. Green pixels are only added on the first and third cells in the existing group, that is, it looks like an adjacent 'frame' must exist for green to be filled.
"""

import numpy as np

def get_red_pixels(grid):
    """Finds the coordinates of all red (2) pixels in the grid."""
    red_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 2:
                red_pixels.append((row_index, col_index))
    return red_pixels

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    red_pixels = get_red_pixels(input_grid)

    for row, col in red_pixels:
        # Check horizontal neighbors
        if col > 0 and col < input_grid.shape[1] - 1:
            if input_grid[row, col - 1] == 0 and input_grid[row,col+1] == 0:
              output_grid[row, col - 1] = 3
              output_grid[row, col + 1] = 3

        # Check vertical neighbors
        if row > 0 and row < input_grid.shape[0] - 1:
            if input_grid[row-1, col] == 0 and input_grid[row+1,col] == 0:
              output_grid[row - 1, col] = 3
              output_grid[row + 1, col] = 3

    return output_grid
```
