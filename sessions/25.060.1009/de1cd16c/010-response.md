# de1cd16c • 010 • example_2 • investigate_coder

---
```python
"""
Count the number of blue pixels in the red quadrant.
"""

import numpy as np

def get_quadrant(grid, row, col):
    """
    Determines the quadrant of a given cell in a grid.

    Args:
        grid: The input grid (2D numpy array).
        row: The row index of the cell.
        col: The column index of the cell.

    Returns:
        An integer representing the quadrant number (0, 1, 2, or 3).
        Quadrants are numbered as follows:
        0 1
        2 3
    """
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2
    if row < mid_row:
        if col < mid_col:
            return 0
        else:
            return 1
    else:
        if col < mid_col:
            return 2
        else:
            return 3

def get_quadrant_bounds(grid, quadrant):
    """
    Returns the row and column boundaries of a given quadrant.

    """
    rows, cols = grid.shape
    mid_row = rows // 2
    mid_col = cols // 2

    if quadrant == 0:
      return (0, mid_row, 0, mid_col)
    if quadrant == 1:
      return (0, mid_row, mid_col, cols)
    if quadrant == 2:
      return (mid_row, rows, 0, mid_col)
    if quadrant == 3:
      return (mid_row, rows, mid_col, cols)

def transform(input_grid):
    # Convert input_grid to numpy array
    grid = np.array(input_grid)

    # Get grid dimensions
    rows, cols = grid.shape

    # determine quadrant bounds
    quadrant_bounds = []
    quadrant_bounds.append(get_quadrant_bounds(grid, 0))
    quadrant_bounds.append(get_quadrant_bounds(grid, 1))
    quadrant_bounds.append(get_quadrant_bounds(grid, 2))
    quadrant_bounds.append(get_quadrant_bounds(grid, 3))
   

    # determine dominant color in each quadrant
    quadrant_colors = []
    for q_bound in quadrant_bounds:
      (min_row, max_row, min_col, max_col) = q_bound
      quad_pixels = grid[min_row:max_row, min_col:max_col]
      unique, counts = np.unique(quad_pixels, return_counts=True)
      dominant_color = unique[np.argmax(counts)]
      quadrant_colors.append(dominant_color)
    
    # identify red quadrant
    red_quadrant_index = -1
    for i in range(len(quadrant_colors)):
        if quadrant_colors[i] == 2:
            red_quadrant_index = i
            break
    
    # count the blue pixels in red quadrant
    blue_count = 0
    if (red_quadrant_index >= 0):
      (min_row, max_row, min_col, max_col) = quadrant_bounds[red_quadrant_index]
      for r in range(min_row, max_row):
        for c in range(min_col, max_col):
          if grid[r,c] == 1:
            blue_count += 1

    return blue_count
```
