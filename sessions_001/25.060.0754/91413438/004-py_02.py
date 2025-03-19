"""
The 3x3 input grid is replicated and tiled in the top-left corner of a 12x12 output grid.
The input is repeated four times in each of rows 1, 2, and 3.
Rows 4, 5, and 6 are the input, padded by 9 columns of white.
The remaining rows and columns are padded with white (0) cells.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 12x12 array filled with 0 (white)
    output_grid = np.zeros((12, 12), dtype=int)

    # Tile Horizontally (first 3 rows)
    for row in range(3):
      for col_multiplier in range(4):
         output_grid[row, col_multiplier * 3 : (col_multiplier + 1) * 3] = input_grid

    # Tile and Pad (next 3 rows)
    for row in range(3,6):
        output_grid[row, 0:3] = input_grid

    return output_grid