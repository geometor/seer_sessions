"""
1. Remove the gray shape: Eliminate all gray (5) pixels from the grid.
2. Shift Left: Move the pre-existing vertical red line (2) two grid cells to the left
3. Shift Down: the pre-existing horizontal red line (2) down two grid cells.
"""

import numpy as np

def find_vertical_line(grid, color):
    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r,c] == color:
                if r + 1 < rows and grid[r+1, c] == color:
                  return c
    return None

def find_horizontal_line(grid, color):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                if c + 1 < cols and grid[r, c+1] == color:
                   return r
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Remove gray shape
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 5:
                output_grid[r, c] = 0

    #find vertical red line
    vertical_line_col = find_vertical_line(input_grid, 2)
    if vertical_line_col is not None:
      for r in range(rows):
        if input_grid[r,vertical_line_col]==2:
          output_grid[r,vertical_line_col]=0
          output_grid[r, vertical_line_col - 2] = 2

    #find horizontal line
    horizontal_line_row = find_horizontal_line(input_grid, 2)
    if horizontal_line_row is not None:
      for c in range(cols):
        if input_grid[horizontal_line_row, c] == 2:
            output_grid[horizontal_line_row,c] = 0
            output_grid[horizontal_line_row + 2, c] = 2

    return output_grid