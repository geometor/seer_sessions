# 25d487eb • 018 • example_3 • investigate_coder

---
```python
"""
Find the red pixel within the green cluster and extend it downwards to the bottom edge of the grid, forming a red column. All other elements of the grid remain unchanged.
"""

import numpy as np

def find_red_pixel(grid):
    # Find the coordinates of the red pixel (value 2).
    red_pixels = np.argwhere(grid == 2)
    if len(red_pixels) > 0:
        return tuple(red_pixels[0])  # Return the first red pixel found
    return None

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find the location of the red pixel.
    red_pixel_coords = find_red_pixel(input_grid)

    if red_pixel_coords:
        row, col = red_pixel_coords
        # Extend the red color downwards.
        for r in range(row + 1, output_grid.shape[0]):
            output_grid[r, col] = 2

    return output_grid
```
