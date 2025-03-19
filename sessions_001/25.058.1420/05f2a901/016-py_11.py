"""
The transformation rule is to cut the input at row index equal to the height of the blue square, starting from top of the red shape.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    # Determine the bounding box.
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the azure (8) object
    azure_min_row, azure_min_col, azure_max_row, azure_max_col = find_object(input_grid, 8)

    # Find the red object (2)
    red_min_row, red_min_col, red_max_row, red_max_col = find_object(input_grid, 2)
    
    #cut point calculation
    if azure_min_row is not None and red_min_row is not None:
        cut_start_row = azure_max_row + 1
        cut_end_row = red_min_row
    
    
        #shift the red object based on cutting position difference
        for r in range(red_min_row, red_max_row +1):
          for c in range(red_min_col, red_max_col+1):
            output_grid[r - (cut_end_row - cut_start_row)][c] = input_grid[r][c]
            if r >= (red_min_row + (cut_end_row - cut_start_row) ):
              output_grid[r][c] = 0

    # Return the modified grid
    return output_grid