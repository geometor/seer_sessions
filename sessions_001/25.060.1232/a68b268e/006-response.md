# a68b268e • 006 • refine_coder

---
```python
"""
Transforms an input grid into an output grid. The transformation involves
identifying a blue line (horizontal or vertical), splitting the grid into two subgrids
based on the line, and concatenating the two subgrids, potentially after a
transposition.
"""

import numpy as np

def get_vertical_line_index(grid):
    # Find the vertical line index
    grid = np.array(grid)
    rows, cols = grid.shape
    for j in range(cols):
      is_line = True
      if grid[0,j] != 1:
        is_line = False
      for i in range(1,rows):
        if grid[i,j] != 1:
          is_line=False
          break
      if is_line:
          return j

    return -1

def get_horizontal_line_index(grid):
    grid = np.array(grid)
    rows, cols = grid.shape
    for i in range(rows):
        is_line = True
        if grid[i, 0] != 1:
          is_line = False
        for j in range(1, cols):
          if grid[i,j] != 1:
            is_line=False
            break
        if is_line:
            return i
    return -1
def transform(input_grid):
    """
    Transforms the input grid by splitting it along a blue line and
    concatenating the resulting subgrids.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify the blue line (horizontal or vertical)
    vertical_line_index = get_vertical_line_index(input_grid)
    horizontal_line_index = get_horizontal_line_index(input_grid)

    # 2. Split the grid into two subgrids
    if vertical_line_index != -1:
        left_subgrid = input_grid[:, :vertical_line_index]
        right_subgrid = input_grid[:, vertical_line_index + 1:]
        output_grid = np.concatenate((right_subgrid, left_subgrid), axis=1)
    elif horizontal_line_index != -1:
        top_subgrid = input_grid[:horizontal_line_index, :]
        bottom_subgrid = input_grid[horizontal_line_index + 1:, :]
        output_grid = np.concatenate((bottom_subgrid, top_subgrid), axis=0)
    else:  # No line found, return input as is (or raise an error)
        output_grid = input_grid


    return output_grid.tolist()
```
