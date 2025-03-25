```python
"""
Identify a rectangular "central object" in the input grid. This object is
defined by a contiguous block of pixels of the same color (the "border color"),
potentially surrounding one or more pixels of a different color (the "inner
color"). Expand the central object outwards by one layer. The border grows, one
layer, maintaining its color.  The inner color also grows to fill the expanded
region, maintaining the overall rectangular shape. The new layer created by
expansion will have the same inner color as the central object, except where
the central object had a border, the new extended layer will have the same
border.  All other pixels in the grid remain unchanged.
"""

import numpy as np

def find_central_object(grid):
    # Find the bounding box of the non-zero pixels
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid
        return None, None, None, None, None, None

    min_row, min_col = np.min(rows), np.min(cols)
    max_row, max_col = np.max(rows), np.max(cols)

    # Get border and inner colors
    border_color = grid[min_row, min_col]
    if (max_row - min_row +1) > 2 and (max_col - min_col + 1) > 2:
      inner_color = grid[min_row + 1, min_col + 1]
    else:
      inner_color = border_color

    return min_row, max_row, min_col, max_col, border_color, inner_color

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    # Find the central object
    min_row, max_row, min_col, max_col, border_color, inner_color = find_central_object(input_grid)

    if min_row is None:  # Handle case where no object is found
        return output_grid

    # Expand the central object
    new_min_row = max(0, min_row - 1)
    new_max_row = min(output_grid.shape[0] - 1, max_row + 1)
    new_min_col = max(0, min_col - 1)
    new_max_col = min(output_grid.shape[1] - 1, max_col + 1)
    
    # Fill expanded border
    for i in range(new_min_row, min_row):
        for j in range(new_min_col, new_max_col+1):
            output_grid[i,j] = border_color
    for i in range(max_row+1, new_max_row+1):
        for j in range(new_min_col, new_max_col+1):
            output_grid[i,j] = border_color    
    for i in range(min_row, max_row +1):
      for j in range(new_min_col, min_col):
        output_grid[i, j] = border_color
      for j in range(max_col + 1, new_max_col+1):
        output_grid[i,j] = border_color

    # Fill the expanded region with the inner color
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if input_grid[i,j] == inner_color:
              output_grid[i,j] = inner_color
            else:
              output_grid[i,j] = border_color
    if inner_color != border_color:
        for i in range(min_row, max_row + 1):
          for j in range(min_col, max_col + 1):
            if input_grid[i,j] == inner_color:
                output_grid[i,j] = input_grid[i,j]
    return output_grid
```