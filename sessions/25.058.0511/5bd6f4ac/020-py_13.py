"""
The transformation identifies non-zero pixels in the input grid, selects a specific non-zero pixel from certain rows, and arranges them into a smaller 3x3 output grid.
"""

import numpy as np

def get_bottom_right_nonzero(grid, row_start, row_end, col_start, col_end):
    """
    Finds the bottom-right non-zero pixel within a specified region of the grid.
    Returns coordinates and value or None if no non-zero pixel.
    """

    for i in range(row_end - 1, row_start -1, -1):
      for j in range(col_end -1, col_start - 1, -1):
        if grid[i,j] != 0:
          return (i,j), grid[i,j]
    return None, 0

def transform(input_grid):
    # Initialize output_grid as 3x3 with zeros
    output_grid = np.zeros((3, 3), dtype=int)

    # Select non-zero bottom-right pixels in specific areas
    _, value1 = get_bottom_right_nonzero(input_grid, 0, 1, 0, 9)  #First Row
    _, value2 = get_bottom_right_nonzero(input_grid, 1, 2, 0, 9) #Second Row
    _, value3 = get_bottom_right_nonzero(input_grid, 2, 9, 0, 9)  #Rest of the rows

    # Change specific output pixel values
    if value1:
        output_grid[0, 2] = value1
    if value2:
        output_grid[1, 0] = value2
    if value3:
        output_grid[2, 2] = value3

    return output_grid