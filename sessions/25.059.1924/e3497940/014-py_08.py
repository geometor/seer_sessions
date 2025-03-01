"""
The transformation rule depends on the presence of a grey (5) column:

1.  **If a grey column exists:** Extract the subgrid to the right of the grey column, excluding any columns that contain grey (5) or white (0) pixels. Remove all grey pixels from the extracted subgrid.
2.  **If no grey column exists:** If there is no grey column, but there is white (0) pixels, return a grid with all zeros and the same dimension as the input.
3. **If no grey column and no white pixels:** If no grey or white pixels, check other colors.
"""

import numpy as np

def find_grey_column(grid):
    """Finds the index of the column that is entirely grey (5)."""
    rows, cols = grid.shape
    for j in range(cols):
        if np.all(grid[:, j] == 5):
            return j
    return -1  # Return -1 if no grey column is found
    
def has_white_pixels(grid):
    """Checks if the grid contains any white (0) pixels."""
    return np.any(grid == 0)

def transform(input_grid):
    """Transforms the input grid based on the presence of a grey column."""
    rows, cols = input_grid.shape
    grey_col_index = find_grey_column(input_grid)

    if grey_col_index != -1:
        # Define extraction boundaries.
        start_col = grey_col_index + 1
        end_col = start_col
        while end_col < cols:
            if any(input_grid[r,end_col] == 5 or input_grid[r, end_col] == 0 for r in range(rows)):
                break
            end_col += 1

        # Extract the sub-grid, and create as all zeros
        output_grid = np.zeros((rows, end_col - start_col))

        # change relevant pixels to values from input, excluding 5
        for r in range(rows):
          for c in range(start_col,end_col):
            if input_grid[r,c] != 5:
              output_grid[r,c-start_col] = input_grid[r,c]

    elif has_white_pixels(input_grid):
        # If no grey column, but white pixels exist, return all zeros.
        output_grid = np.zeros_like(input_grid)
        
    else:
      output_grid = np.zeros_like(input_grid)

    return output_grid