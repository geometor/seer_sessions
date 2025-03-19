"""
1.  **Identify Non-Zero Pixels:** Find all pixels in the input grid that have a value other than 0.
2.  **Horizontal Line Extension**: For each row containing a non-zero pixel, extend a horizontal line of the same color across the entire row in the output grid.
3. **Vertical Line Extension (Limited):** If a non-zero pixel does not extend vertically beyond 1, it is extended.

"""

import numpy as np

def find_non_zero_pixels(grid):
    """Finds the coordinates and values of non-zero pixels in a grid."""
    non_zero_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value != 0:
                non_zero_pixels.append(((row_index, col_index), value))
    return non_zero_pixels

def extend_horizontally(grid, row, value):
    """Extends a horizontal line across the entire row."""
    for col_index in range(grid.shape[1]):
        grid[row, col_index] = value

def extend_vertically(grid, col, value, start_row, end_row):
    """Extends a line vertically from a given column"""
    for i in range(start_row, end_row + 1):
       grid[i,col] = value
    

def transform(input_grid):
    # Initialize output grid as all zeros
    output_grid = np.zeros_like(input_grid)
    input_grid = np.array(input_grid)

    non_zero_pixels = find_non_zero_pixels(input_grid)

    # Extend lines horizontally
    for (row, col), value in non_zero_pixels:
      extend_horizontally(output_grid, row, value)
    
    # Extend some lines vertically
    for (row, col), value in non_zero_pixels:
      if output_grid[row,col] == value:
        row_values = input_grid[row,:]
        if np.count_nonzero(row_values) == 1:
          # find extents for vertical line
          found = False
          for r_idx in range(input_grid.shape[0]):
            if input_grid[r_idx,col] != 0:
               if not found:
                  start_row = r_idx
                  found = True
               end_row = r_idx
          
          extend_vertically(output_grid, col, value, start_row, end_row)
        

    return output_grid