"""
1.  **Extend Height:** The input grid's height (number of rows) is increased to 3.
2.  **Copy first column:** The first column from the input grid is examined.
3.  **Fill color down:** The color of each value in the first column of the input grid, is copied to the output grid, stacked vertically by the new height of the grid.
4.  **Remainder of grid:** The rest of the grid, columns 2-6, remain 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with new height and same width, filled with 0s.
    input_rows, input_cols = input_grid.shape
    output_grid = np.zeros((3, input_cols), dtype=int)
    
    # Fill the new grid
    for j in range(input_cols):
      if j == 0:
        for i in range(3):
          output_grid[i,j] = input_grid[0,j]
      else:
        for i in range(3):
          output_grid[i,j] = input_grid[0,j]


    return output_grid