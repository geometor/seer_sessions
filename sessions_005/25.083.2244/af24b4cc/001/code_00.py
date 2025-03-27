"""
Extracts specific colored pixels from the input grid and places them in a smaller output grid. The pixels are taken from the middle row of colored regions within the 2nd, 5th, 7th, and 9th columns of the input, and they are positioned in the 2nd row and columns 2-5 of the output grid.
"""

import numpy as np

def find_colored_region(input_grid, col):
    """Finds a contiguous colored region in a specific column."""
    rows, _ = input_grid.shape
    start_row = -1
    end_row = -1
    
    for row in range(rows):
      if input_grid[row, col] != 0:
        if start_row == -1:
          start_row = row
        end_row = row

    if start_row != -1:
        return start_row, end_row
    
    return -1, -1

def transform(input_grid):
    # Initialize output_grid as 4x5 filled with 0s
    output_grid = np.zeros((4, 5), dtype=int)

    # Define target columns in the input grid (2nd, 5th, 7th, 9th) - indexing from 0
    target_columns = [1, 4, 6, 8]

    # Iterate through target columns
    for i, col in enumerate(target_columns):
        # Find the colored region in the specified column
        start_row, end_row = find_colored_region(input_grid, col)
        
        # Extract middle pixel from the colored block if rows 2,3,4 have data
        if 1 <= start_row and end_row <= 3:  # Check the region to be at the intersection of rows 2,3,4 (indexed as 1,2,3)
            middle_row = 2
            pixel_value = input_grid[middle_row, col]
            # Place the extracted pixel in the output grid
            output_grid[1, i + 1] = pixel_value  # +1 to shift columns in the output (columns 2-5)

    return output_grid