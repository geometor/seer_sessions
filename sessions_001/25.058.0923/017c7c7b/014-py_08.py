"""
1. Identify: Locate the vertical line of blue (1) pixels in the input grid.
2. Substitute: Change the color of all pixels in the blue line from blue (1) to red (2).
3. Expand: Add three rows of red (2) to the bottom of the output.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find columns that have at least one pixel of the specified color
    cols_with_color = np.any(grid == color, axis=0)
    
    # Ensure that all elements in these columns, that are not the background color, equal to color
    for col_idx in np.where(cols_with_color)[0]:
        column = grid[:, col_idx]
        if not np.all((column == color) | (column == 0)):  # Assuming 0 is background
           return None
    
    # return the index
    return np.where(cols_with_color)[0]

def transform(input_grid):
    # Initialize output_grid as a copy of input and change the color
    output_grid = input_grid.copy()
    output_grid[output_grid == 1] = 2

    # Find the vertical line of blue pixels
    blue_line_cols = find_vertical_line(input_grid, 1)
    
    # Add three rows for the red
    if blue_line_cols is not None:
       num_rows_to_add = 3
       rows, cols = output_grid.shape
       new_output_grid = np.zeros((rows + num_rows_to_add, cols), dtype=int)
       new_output_grid[:rows,:] = output_grid
       for col in blue_line_cols:
          new_output_grid[rows:,col] = 2
       output_grid = new_output_grid

    return output_grid