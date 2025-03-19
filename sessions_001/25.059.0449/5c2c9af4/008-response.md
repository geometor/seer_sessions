# 5c2c9af4 • 008 • refine_coder

---
```python
"""
The transformation starts with the original input grid. Then, for each azure (8) pixel in the input grid, it extends a vertical line of azure downwards from the azure pixel's row to the bottom of the grid.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds the coordinates of all azure (8) pixels in the grid."""
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)  # Start with the original input grid

    azure_pixels = get_azure_pixels(input_grid)

    # Vertical Extension
    for pixel in azure_pixels:
        row, col = pixel
        output_grid[row:, col] = 8

    return output_grid
```
