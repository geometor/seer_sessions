"""
Copies the input grid to the output grid, preserving the outer frame of '6' and '7' pixels.
The seventh row from the bottom and the seventh column from the right are modified:
'7's in these row/column are changed to '6's, unless they are part of the original outer frame.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    # Modify the seventh row from the bottom
    row_index = rows - 7
    if 0 < row_index < rows -1 :
      for c in range(1, cols -1):
        if output_grid[row_index, c] == 7:
          output_grid[row_index, c] = 6

    # Modify the seventh column from the right
    col_index = cols - 7
    if 0 < col_index < cols - 1:
      for r in range(1, rows -1):
          if output_grid[r, col_index] == 7:
            output_grid[r, col_index] = 6

    return output_grid.tolist()