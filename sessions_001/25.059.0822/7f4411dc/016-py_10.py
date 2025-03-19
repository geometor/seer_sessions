"""
1. Identify all gray (5) pixels in the input grid.
2. Determine the minimal bounding rectangle that can enclose main object of grey color.
3. Remove any isolated gray pixels from the input grid if it is at the border.
4. Keep the internal block of grey and consolidate.
5. Change all other pixels, outside of the consolidated gray rectangle, to white (0).
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No pixels of the specified color found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    
    # Get the bounding box of grey pixels
    bounding_box = get_bounding_box(input_grid, 5)
    
    if bounding_box:
      (min_row, min_col), (max_row, max_col) = bounding_box

      # create the internal grey object
      for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col+1):
          output_grid[i,j] = 5

    # set to zero all cells that are not in the box
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if not (bounding_box and min_row <= i <= max_row and min_col <= j <= max_col):
                output_grid[i, j] = 0
    

    return output_grid