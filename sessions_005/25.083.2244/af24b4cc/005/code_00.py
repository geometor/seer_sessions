"""
Extracts specific colored pixels from the input grid and places them in a smaller output grid. Pixels are taken from specific rows within the 2nd, 5th, 7th, and 9th columns of the input, based on whether the colored block starts within the upper region (rows 2-4) or lower region (rows 6-8). These pixels are placed in the 2nd row and columns 2-5 of the output if from the upper region, or 3rd row and columns 2-5 of the output if from the lower region.
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
        start_row, _ = find_colored_region(input_grid, col)
        
        # Check if the colored region intersects with upper or lower region
        if start_row != -1:  # ensure we found a colored block
            if 1 <= start_row <= 3:  # Upper region (rows 2-4, indices 1-3)
                pixel_value = input_grid[1, col]  # Extract from row 2 (index 1)
                output_grid[1, i + 1] = pixel_value  # Place in output row 2 (index 1)
            elif 5 <= start_row <= 7:  # Lower region (rows 6-8, indices 5-7)
                pixel_value = input_grid[5, col]  # Extract from row 6 (index 5)
                output_grid[2, i + 1] = pixel_value # Place in output row 3 (index 2)

    return output_grid