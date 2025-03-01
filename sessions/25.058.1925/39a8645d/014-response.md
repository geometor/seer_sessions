# 39a8645d • 014 • refine_coder

---
```python
"""
The transformation rule extracts all yellow (4) pixels from the input grid and reconstructs their relative positions in the output grid. The output grid's dimensions are determined by the maximum row and column differences between the yellow pixels in the input, plus one. The output grid uses a white (0) background.
"""

import numpy as np

def find_yellow_pixels(grid):
    """Finds coordinates of all yellow (4) pixels in the grid."""
    return np.argwhere(grid == 4)

def transform(input_grid):
    """Transforms the input grid by extracting yellow pixels and preserving their relative positions."""

    # Find coordinates of yellow pixels.
    yellow_pixels = find_yellow_pixels(input_grid)

    # If no yellow pixels, return an empty grid (or a 1x1 white grid).
    if len(yellow_pixels) == 0:
        return np.zeros((1, 1), dtype=int)

    # Calculate the dimensions of the output grid.
    min_row = np.min(yellow_pixels[:, 0])
    max_row = np.max(yellow_pixels[:, 0])
    min_col = np.min(yellow_pixels[:, 1])
    max_col = np.max(yellow_pixels[:, 1])

    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    
    # initialize output
    output_grid = np.zeros((output_height, output_width), dtype=int)


    # Populate the output grid with yellow pixels, adjusting for relative positions.
    for r, c in yellow_pixels:
        output_grid[r - min_row, c - min_col] = 4

    return output_grid
```
