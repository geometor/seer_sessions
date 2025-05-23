"""
Identifies a cross-shaped pattern of colored pixels (red, green, yellow) in the input grid. 
Locates the red pixel within the cross. 
Extends the red pixel horizontally by adding one red pixel to its left and one to its right.
Preserves all other colored pixels in their original positions.
"""

import numpy as np

def find_cross_center(grid):
    # Find all non-zero pixels
    non_zero_indices = np.argwhere(grid != 0)

    # If no non-zero pixels, return None, None
    if len(non_zero_indices) == 0:
      return None,None

    # Calculate the center of the non-zero pixels
    center_row = np.mean(non_zero_indices[:, 0]).astype(int)
    center_col = np.mean(non_zero_indices[:, 1]).astype(int)
    return center_row, center_col
    
def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find the center of cross
    center_row, center_col = find_cross_center(input_grid)
    if center_row is None:
        return output_grid

    # find red pixel
    if input_grid[center_row, center_col] != 0: # it is not the center
       # scan cross
       for i in range(center_row -2, center_row+3):
          if input_grid[i,center_col] == 2:
             center_row = i
             break
       for j in range(center_col - 2, center_col + 3):
          if input_grid[center_row, j] == 2:
             center_col = j
             break

    if input_grid[center_row, center_col] == 2:
        # Extend red pixel horizontally
        if center_col > 0:
            output_grid[center_row, center_col - 1] = 2  # Add red pixel to the left
        if center_col < cols - 1:
            output_grid[center_row, center_col + 1] = 2  # Add red pixel to the right

    return output_grid