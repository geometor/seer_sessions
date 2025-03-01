# 3618c87e • 005 • refine_coder

---
```python
"""
Swaps a gray pixel (value 5) with the pixel located two rows below it in the same column, provided the target is not black.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return as (row, col)
    return None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the coordinates of the gray pixel (5)
    gray_coords = find_pixel(input_grid, 5)

    # If gray pixel is found, proceed with the swap
    if gray_coords:
        # Calculate the target coordinates for the swap (two rows below)
        target_row = gray_coords[0] + 2

        # Check if the target row is within the grid boundaries and not black
        if target_row < output_grid.shape[0] and output_grid[target_row, gray_coords[1]] != 0 :
            # Get current color at target.
            target_color = output_grid[target_row, gray_coords[1]]

            # perform the swap
            output_grid[target_row, gray_coords[1]] = 5
            output_grid[gray_coords[0], gray_coords[1]] = target_color

    return output_grid
```
