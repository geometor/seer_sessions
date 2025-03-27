"""
Transforms an input grid by rearranging "outlier" pixels (those not orange (7) or azure (8)) within a defined central area, while preserving a base row of azure pixels.
The transformation shifts the colors of non-orange pixels down by 1 row and one column within two-row sliding windows, setting out-of-bounds pixels to orange.
"""

import numpy as np

def get_central_area_indices(grid):
    """
    Finds the row indices that define the central area
    """
    for i in range(len(grid) -1, -1, -1):
        if not np.all(grid[i] == 8):
            return 0, i
    return 0,0 # should never happen given constraints

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    top, bottom = get_central_area_indices(input_grid)

    # Iterate through two-row windows in central area
    for i in range(top, bottom):
        for j in range(cols):
          if input_grid[i,j] != 7 and input_grid[i,j] != 8:
            # shift cell value
            new_row = i + 1
            new_col = j + 1

            # boundary check
            if new_row > bottom:
                # if out of bounds below, remove (set to 7)
                output_grid[i, j] = 7
            elif new_col >= cols:
              output_grid[i,j] = 7
            else:
              # shift within bounds: swap the values, setting the original position to orange
              if output_grid[new_row, new_col] == 7 or output_grid[new_row, new_col] == 8:
                output_grid[new_row, new_col] = input_grid[i, j]
                output_grid[i,j] = 7
              
    return output_grid