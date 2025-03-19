# b8cdaf2b • 022 • refine_coder

---
```python
"""
Identify yellow (4) pixels in the bottom row. Move the yellow block two rows up, but do not change any existing pixels of the same color, or any new position that contains a value other than blank (0).
"""

import numpy as np

def get_yellow_pixels(grid):
    """Finds the coordinates of yellow (4) pixels in the bottom row."""
    yellow_pixels = []
    rows, cols = grid.shape
    for x in range(cols):
        if grid[rows - 1, x] == 4:
            yellow_pixels.append((rows - 1, x))
    return yellow_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # get yellow pixels
    yellow_pixels = get_yellow_pixels(input_grid)

    # move blocks up
    for row, col in yellow_pixels:
        # move up only if cell is 0
        if output_grid[row-2, col] == 0:
            output_grid[row - 2, col] = 4
            output_grid[row,col] = 0

    return output_grid
```
