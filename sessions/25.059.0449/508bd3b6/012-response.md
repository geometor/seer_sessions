# 508bd3b6 • 012 • refine_coder

---
```python
"""
The transformation rule takes each azure pixel and expands it into an "L" shape of green pixels to the right and down, stopping when there is no available cell, or they are out of the grid. The red block at the bottom remains unchanged.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color).tolist()

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    azure_pixels = find_pixels_by_color(input_grid, 8)

    for row, col in azure_pixels:
        # Generate green pixel to the right
        if col + 1 < output_grid.shape[1] :
            output_grid[row, col + 1] = 3

            #extend to edge
            for i in range(col + 2, output_grid.shape[1]):
                if output_grid[row,i] == 0:
                    output_grid[row, i] = 3
                else: break

        # Generate green pixels downwards
        if row + 1 < output_grid.shape[0] :
            output_grid[row + 1,col] = 3

            #extend to edge
            for i in range(row + 2, output_grid.shape[0]):
                if output_grid[i,col] == 0:
                    output_grid[i, col] = 3
                else: break

    return output_grid
```
