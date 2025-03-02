# 253bf280 • 014 • refine_coder

---
```python
"""
1.  **Copy Azure Pixels:** Copy all azure (8) pixels from the input grid to the output grid, maintaining their original positions.

2.  **Extend with Green Lines:** For each azure pixel in the *output* grid:
    *   Create a vertical line of green (3) pixels centered on the azure pixel.
    *   The total length of the green line (including the azure pixel) should be 5.
    *   The extension should only happen if it doesn't go out of the grid's boundaries.
    * If placing a green pixel would overwrite an existing azure, then that green pixel is not placed.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels in the grid."""
    return np.argwhere(grid == 8)

def can_extend(grid, row, col):
    """Checks if a green line of length 5 can be created at the given position, without overwriting azure."""
    rows, cols = grid.shape
    # Check bounds
    if row - 2 < 0 or row + 2 >= rows:
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
        if can_extend(output_grid, row, col):
            if output_grid[row - 1, col] != 8:
                output_grid[row - 1, col] = 3  # Up 1
            if output_grid[row + 1, col] != 8:
                output_grid[row + 1, col] = 3  # Down 1
            if row - 2 >= 0 and output_grid[row - 2, col] != 8:
                output_grid[row - 2, col] = 3 # Up 2
            if row + 2 < rows and output_grid[row + 2, col] != 8:
                output_grid[row + 2, col] = 3  # Down 2

    return output_grid
```
