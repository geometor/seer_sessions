"""
1.  **Identify the central vertical line:** Locate the vertical line of blue (1) pixels running down the center (column index 3, starting from 0) of the input grid.

2. **Create a new grid, smaller than the first.** The new grid should have the same height as the input grid and width of 3.

3.  **Transfer and Transform.** Create the new output grid based on the original central vertical line of blue pixels as follows, working from left to right in the output, one column at a time, starting at the left-most column:
    *   Original column to left of the blue line in the input, replace all the maroon pixels with white and the white pixels with azure.
    *   Original blue line - replace all the blue pixels with white.
    *   Original column to the right of the blue line in the input, replace all the maroon pixels with white and the white pixels with azure.
"""

import numpy as np

def find_blue_line(grid):
    # Find the column index of the vertical blue line.
    height = len(grid)
    width = len(grid[0])
    for j in range(width):
        is_blue_line = True
        for i in range(height):
            if grid[i][j] != 1:
                is_blue_line = False
                break
        if is_blue_line:
            return j
    return -1  # Return -1 if no blue line is found

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    output_grid = np.zeros((height, 3), dtype=int)

    # Find the blue line
    blue_line_col = find_blue_line(input_grid) # this should be index 3

    # change output pixels
    # process column to left of blue line
    if blue_line_col > 0:
      for i in range(height):
          if input_grid[i][blue_line_col - 1] == 9:
              output_grid[i][0] = 0
          elif input_grid[i][blue_line_col-1] == 0:
              output_grid[i][0] = 8

    # process the blue line itself, turning to white
    for i in range(height):
        output_grid[i][1] = 0

    # process column to right of blue line
    if blue_line_col < width - 1:
        for i in range(height):
          if input_grid[i][blue_line_col+1] == 9:
            output_grid[i][2] = 0
          elif input_grid[i][blue_line_col+1] == 0:
              output_grid[i][2] = 8

    return output_grid.tolist()