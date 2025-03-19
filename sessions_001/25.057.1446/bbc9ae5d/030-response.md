# bbc9ae5d • 030 • refine_coder

---
```python
"""
The transformation rule identifies the single orange pixel (value 7) in the input grid and replicates it to form a 3x3 orange square in the output grid, with the top-left corner of the square at the location of the original orange pixel. The output grid has the same dimension as the input, and all 0 valued pixels retain their location.
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

    # Initialize output grid with same dimensions and filled with white (0)
    output_grid = np.zeros_like(input_grid, dtype=int)

    # Find the orange pixel (value 7)
    orange_pixel_coords = find_pixel_by_value(input_grid, 7)

    # Replicate orange square
    if orange_pixel_coords is not None:
        row, col = orange_pixel_coords
        for i in range(row, min(row + 3, output_grid.shape[0])):
            for j in range(col, min(col + 3, output_grid.shape[1])):
                output_grid[i, j] = 7

    # Copy all zero pixels
    for r in range(input_grid.shape[0]):
      for c in range(input_grid.shape[1]):
        if input_grid[r,c] == 0:
          output_grid[r,c] = 0
    return output_grid
```
