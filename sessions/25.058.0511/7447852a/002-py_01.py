"""
Examine the input grid. The red (2) pixels are the focus.
If a red pixel is immediately adjacent to a red pixel, it might turn to yellow (4), either horizontally or vertically.
If a red pixel has a direct horizontal or vertical neighbor, that is also red, under the following condition:
- if a red pixel is on the edge, it will have at maximum, 2 vertical or 2 horizontal neighbours
- if a red pixel is in the middle, it will have at maximum, 1 horizontal or 1 vertical neighbours.
- if a red pixel satisfy any of these condition, it is converted to yellow (4).
Create the output grid by copying the input grid, changing some red (2) to yellow(4), according to previous rules. All other pixels remain unchanged.
"""

import numpy as np

def count_adjacent_reds(grid, row, col):
    """Counts the number of red neighbors (horizontal and vertical) for a given cell."""
    count = 0
    rows, cols = grid.shape
    if row > 0 and grid[row-1, col] == 2:
        count += 1
    if row < rows - 1 and grid[row+1, col] == 2:
        count += 1
    if col > 0 and grid[row, col-1] == 2:
        count += 1
    if col < cols - 1 and grid[row, col+1] == 2:
        count += 1
    return count

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 2: #if red pixel
              adjacent_reds = count_adjacent_reds(input_grid, row, col)
              if 0 < row < rows -1: # middle rows
                if adjacent_reds <=1 :
                  output_grid[row,col] = 4
              elif (row == 0 or row == rows-1):
                if adjacent_reds <=2:
                  output_grid[row, col] = 4
    return output_grid