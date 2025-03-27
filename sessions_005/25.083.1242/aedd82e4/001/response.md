```python
"""
Locate red pixel(s) in the grid. Change the color from red (2) to blue (1) if certain adjacency condition is met. Specifically, change the lower-right most red pixel that is adjacent to at least one white pixel.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (including diagonals)."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                adjacent.append((i, j, grid[i, j]))
    return adjacent

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    red_pixels = []

    # Iterate through each pixel to find red pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
                red_pixels.append((r, c))

    # check red pixels and see if they are next to white pixels.
    target_pixel = None
    for r, c in reversed(red_pixels):
      adjacent_pixels = get_adjacent_pixels(output_grid,r,c)
      for ar, ac, val in adjacent_pixels:
        if val == 0:
          target_pixel = (r,c)
          break
      if target_pixel:
        break
          
    # change output pixels
    if target_pixel:
      output_grid[target_pixel[0],target_pixel[1]] = 1

    return output_grid
```