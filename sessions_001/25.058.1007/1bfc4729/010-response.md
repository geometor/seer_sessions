# 1bfc4729 • 010 • example_2 • investigate_coder

---
```python
"""
Transforms an input grid by expanding a blue pixel (1) and a yellow pixel (4) into regions. The blue pixel expands upwards and downwards to the row before yellow, filling entire rows. The yellow pixel expands downwards and upwards to row below blue, similarly filling entire rows.
"""

import numpy as np

def find_pixel(grid, color_value):
    """Finds the coordinates of a pixel with a specific color value."""
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == color_value:
                return (r, c)
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find blue and yellow pixels
    blue_pos = find_pixel(input_grid, 1)
    yellow_pos = find_pixel(input_grid, 4)

    # Handle cases where blue or yellow might be missing
    if blue_pos is None and yellow_pos is not None:
      for r in range(yellow_pos[0]):
          output_grid[r,:] = 0
      for r in range(yellow_pos[0], output_grid.shape[0]):
          output_grid[r,:] = 4
      return output_grid

    if yellow_pos is None and blue_pos is not None:
      for r in range(blue_pos[0]+1):
        output_grid[r,:] = 1
      for r in range(blue_pos[0] + 1, output_grid.shape[0]):
          output_grid[r,:] = 0
      return output_grid

    if (blue_pos is None) and (yellow_pos is None):
       return output_grid

    # Blue expansion
    if blue_pos:
        for r in range(blue_pos[0] + 1):
            output_grid[r, :] = 1
        for r in range(blue_pos[0]+1, yellow_pos[0]):
          output_grid[r,:] = 0

    # Yellow expansion
    if yellow_pos:
        for r in range(yellow_pos[0], input_grid.shape[0]):
            output_grid[r, :] = 4
        for r in range(blue_pos[0]+1,yellow_pos[0]):
          output_grid[r,:] = 0

    return output_grid
```
