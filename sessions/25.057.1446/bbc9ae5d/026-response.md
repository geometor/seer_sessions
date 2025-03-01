# bbc9ae5d • 026 • example_5 • investigate_coder

---
```python
"""
The transformation rule identifies the orange pixel (value 7) in the input grid's top-left corner and replicates it to form a 3x3 orange square in the output grid, while also copying 0 values at the corresponding positions and filling the rest with white.
"""

import numpy as np

def find_pixel_by_value(grid, value):
    """Finds the coordinates of the first pixel with a given value."""
    coords = np.where(grid == value)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize output grid as 3x6 filled with white (0)
    output_grid = np.zeros((3, 6), dtype=int)

    # Find the orange pixel (value 7)
    orange_pixel_coords = find_pixel_by_value(input_grid, 7)

    # replicate first pixel in output
    if orange_pixel_coords is not None:
       for i in range(3):
           for j in range(3):
              output_grid[i,j] = 7
    # Copy the white (0) values and place at proper locations

    for x in range(input_grid.shape[1]):
        if input_grid[0,x] == 0:
          output_grid[0,x] = 0

    return output_grid
```
