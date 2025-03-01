# 74dd1130 • 024 • refine_coder

---
```python
"""
The transformation involves iterating through all possible 3x3 subgrids within the input grid and applying a specific pixel-swapping logic within each subgrid. The pixel-swapping logic is as follows:
1. Top-left pixel swaps with top-right.
2. Bottom-left pixel swaps with bottom-right.
3. Top-middle pixel swaps with left-middle.
4. Bottom-middle pixel swaps with right-middle.
The center pixel remains unchanged.
"""

import numpy as np

def _swap_pixels(grid, row, col):
    # Swap top-left and top-right pixels.
    grid[row, col], grid[row, col + 2] = grid[row, col + 2], grid[row, col]

    # Swap bottom-left and bottom-right pixels.
    grid[row + 2, col], grid[row + 2, col + 2] = grid[row + 2, col + 2], grid[row + 2, col]

    # Swap top-middle and left-middle pixels.
    grid[row, col + 1], grid[row + 1, col] = grid[row + 1, col], grid[row, col + 1]

    # Swap bottom-middle and right-middle pixels.
    grid[row + 2, col + 1], grid[row + 1, col + 2] = grid[row + 1, col + 2], grid[row + 2, col + 1]
    return grid

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through all possible 3x3 subgrids.
    for row in range(height - 2):
        for col in range(width - 2):
            # Apply the pixel-swapping transformation to the current 3x3 subgrid.
            output_grid = _swap_pixels(output_grid, row, col)

    return output_grid
```
