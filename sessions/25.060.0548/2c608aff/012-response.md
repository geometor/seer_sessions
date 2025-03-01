# 2c608aff • 012 • refine_coder

---
```python
"""
1. Identify the background: The background is red (2) and remains unchanged.
2. Locate the azure pixel: Find the single azure (8) pixel within the input grid.
3. Vertical Expansion: Transform the azure pixel into a vertical line of azure pixels. 
   The line starts at the row where the azure pixel was found.  The bottom of the line
   will be in the row one above the final row of the input. The azure line does not
   change columns.
4. Return the modified grid: The output grid is identical to the input grid except for
   the expanded azure line.
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
        # Expand the azure pixel downwards to the second-to-last row
        for i in range(r, output_grid.shape[0] - 1):
           output_grid[i, c] = 8

    return output_grid
```
