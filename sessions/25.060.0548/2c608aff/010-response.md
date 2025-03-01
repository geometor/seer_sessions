# 2c608aff • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1. Identify a blue (1) 3x3 rectangle and an azure (8) pixel.
2. The background is red (2) and remains unchanged.
3. The azure (8) pixel expands vertically upwards, transforming into a vertical line of azure (8) pixels. 
   The expansion starts from row 6 and goes until row 9, inclusive, staying in the same column.
4. Return the changed grid.
"""

import numpy as np

def find_object(grid, color, shape_type=None, dimensions=None):
    """Finds an object of specified color, and optionally, shape and dimensions."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                if shape_type == 'rectangle' and dimensions:
                    h, w = dimensions
                    if r + h <= grid.shape[0] and c + w <= grid.shape[1]:
                        if np.all(grid[r:r+h, c:c+w] == color):
                            return r, c, h, w
                elif shape_type == 'pixel':
                    return r, c, 1, 1
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the azure pixel
    azure_pixel = find_object(input_grid, 8, 'pixel')

    if azure_pixel:
        r, c, _, _ = azure_pixel
        # Expand the azure pixel upwards
        for i in range(6, 10):
           output_grid[i, c] = 8

    return output_grid
```
