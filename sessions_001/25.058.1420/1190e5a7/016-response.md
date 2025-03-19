# 1190e5a7 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation identifies blue (1) lines in the input grid, which form a grid-like structure separating areas of green (3). 
The transformation extracts the smallest green area.
"""

import numpy as np

def find_blue_lines(grid):
    """Finds the row and column indices of blue (1) pixels."""
    rows, cols = np.where(grid == 1)
    return rows, cols

def extract_green_area(grid, rows, cols):
    """Extracts the smallest green area, starting from top-left."""
    
    min_row = np.min(rows)
    min_col = np.min(cols)
    
    # Find dimensions of smallest rectangle
    # Find the next blue pixel to the right
    right_blue = cols[cols > min_col]
    if right_blue.size > 0:
      col_width = np.min(right_blue)-min_col
    else:
      return None # should never happen in the valid cases

    # Find the next blue pixel below
    down_blue = rows[rows > min_row]
    if down_blue.size > 0:
      row_height = np.min(down_blue)-min_row
    else:
      return None # should never happen

    start_row = min_row - (row_height - 1)
    
    start_col = min_col - (col_width -1)

    subgrid = grid[start_row:start_row + row_height, start_col:start_col + col_width]
    return subgrid


def transform(input_grid):
    """Extracts the smallest green subgrid defined by blue lines."""
    # Find blue line coordinates
    rows, cols = find_blue_lines(input_grid)

    # Extract the green area
    output_grid = extract_green_area(input_grid, rows, cols)
    if output_grid is None:
        return np.zeros((1,1))

    return output_grid
```
