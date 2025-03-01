# af902bf9 • 002 • example_3 • investigate_coder

---
```python
"""
Locate yellow pixels, and fill red pixels between them, and the shape of the fill is defined by the minimum rectangle that encloses them.
"""

import numpy as np

def get_yellow_pixels(grid):
    # Find coordinates of all yellow pixels.
    yellow_pixels = np.argwhere(grid == 4)
    return yellow_pixels

def fill_between(input_grid, yellow_pixels):
    #Create output grid
    output_grid = np.copy(input_grid)

    if len(yellow_pixels) == 0:
      return output_grid

    if len(yellow_pixels) == 1:
        return output_grid
    
    # Find min and max row and col
    min_row = np.min(yellow_pixels[:, 0])
    max_row = np.max(yellow_pixels[:, 0])
    min_col = np.min(yellow_pixels[:, 1])
    max_col = np.max(yellow_pixels[:, 1])

    # fill the area with red
    output_grid[min_row:max_row + 1, min_col:max_col + 1] = np.where(
        (output_grid[min_row:max_row + 1, min_col:max_col + 1] == 0), 2, output_grid[min_row:max_row + 1, min_col:max_col + 1])
    
    return output_grid

def transform(input_grid):
    # Find all yellow pixels
    yellow_pixels = get_yellow_pixels(input_grid)

    # Fill between the yellow pixels with red
    output_grid = fill_between(input_grid, yellow_pixels)

    return output_grid
```
