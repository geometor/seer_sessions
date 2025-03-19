# 623ea044 • 016 • example_3 • investigate_coder

---
```python
"""
Identify the single azure (8) pixel in the input grid.  Expand diagonally from this seed pixel,
creating azure (8) pixels outwards in all four diagonal directions (up-left, up-right, down-left, down-right).
Continue the diagonal expansion until the edge of the grid is reached in each direction.
"""

import numpy as np

def find_seed_pixel(grid):
    # Find the coordinates of the azure (8) pixel.
    rows, cols = np.where(grid == 8)
    if len(rows) > 0:  # Check if an 8 was found
       return rows[0], cols[0]
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.zeros_like(input_grid)
    
    # output_grid[:] = input_grid[:] # start with a zero grid rather than copying input

    # Find the seed pixel.
    seed_coords = find_seed_pixel(input_grid)
    if seed_coords is None:
        return output_grid # return if no seed pixel

    seed_row, seed_col = seed_coords

    # set seed pixel
    output_grid[seed_row, seed_col] = 8

    # Get grid dimensions.
    height, width = input_grid.shape

    # Expand diagonally.
    for i in range(1, max(height, width)):
        # Up-left
        if seed_row - i >= 0 and seed_col - i >= 0:
            output_grid[seed_row - i, seed_col - i] = 8
        # Up-right
        if seed_row - i >= 0 and seed_col + i < width:
            output_grid[seed_row - i, seed_col + i] = 8
        # Down-left
        if seed_row + i < height and seed_col - i >= 0:
            output_grid[seed_row + i, seed_col - i] = 8
        # Down-right
        if seed_row + i < height and seed_col + i < width:
            output_grid[seed_row + i, seed_col + i] = 8

    return output_grid
```
