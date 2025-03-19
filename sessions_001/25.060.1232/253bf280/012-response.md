# 253bf280 • 012 • refine_coder

---
```python
"""
1.  **Copy:** Copy all azure (8) pixels from the input grid to the output grid.
2. **Extend:** For azure pixels in the input grid where a vertical line of 4 green blocks, centered on the azure can be created without going out of bounds or overlapping with other azure blocks, add a vertical line of green (3) pixels centered vertically on the azure pixel, creating a total length of four green pixels. If the azure pixel is too close to the top or bottom edge, OR adjacent vertically or horizontally, then the green extension is not created.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels in the grid."""
    return np.argwhere(grid == 8)

def can_extend(grid, row, col):
    """Checks if a green line of length 4 can be created at the given position."""
    rows, cols = grid.shape
    # Check bounds and azure neighbors
    if row - 1 < 0 or row + 2 >= rows:
        return False

    for r in range(row - 1, row + 2):
        if grid[r,col] == 8 and r != row:
          return False

    return True

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    output_grid = np.copy(input_grid)
    azure_pixels = get_azure_pixels(input_grid)
    rows, cols = input_grid.shape

    for row, col in azure_pixels:
      # copy existing azure
        output_grid[row, col] = 8

        # grow green shoots up and down, only if possible.
        if can_extend(output_grid,row,col):
            output_grid[row - 1, col] = 3
            output_grid[row + 1, col] = 3
            if row -2 >= 0:
                output_grid[row-2, col] = 3
            if row + 2 < rows:
                output_grid[row + 2, col] = 3

    return output_grid
```
