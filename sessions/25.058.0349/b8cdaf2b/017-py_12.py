"""
1.  **Identify the Colored Block:** Find the contiguous rectangular block of non-zero colored pixels in the input grid.
2.  **Locate Top Row:** Determine the row index of the top row of the colored block.
3. **Preserve Colored Block:** The output contains the colored block in the same configuration and location as in the input.
4.  **Add Blue Markers:** Add two blue pixels (color 1) to the grid.
    *   One blue pixel is placed in the first column (index 0) of the row immediately above the colored block's top row.
    *   The other blue pixel is placed in the last column (index -1) of the same row as the first marker.
5.  **All other cells are black (0).**
"""

import numpy as np

def transform(input_grid):
    #copy input to output
    output_grid = np.copy(input_grid)
    #find the first row with non-zero values
    first_row = 0
    for i, row in enumerate(grid):
      if np.any(row != 0):
        first_row = i
        break

    #place the blue pixels
    output_grid[first_row-1, 0] = 1
    output_grid[first_row-1, -1] = 1

    return output_grid