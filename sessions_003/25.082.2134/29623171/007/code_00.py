"""
Copies a block of non-gray, non-white pixels from above the top-most gray line to the area below the bottom-most gray line. The source block starts to the right of the rightmost vertical gray stripe. The copied block is repeated downwards until the bottom of the output grid is reached.
"""

import numpy as np

def find_horizontal_gray_lines(grid):
    """Finds the row indices of all horizontal lines of 5s."""
    gray_lines = []
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 5):
            gray_lines.append(r)
    return gray_lines

def find_rightmost_gray_stripe(grid):
    """Finds the column index of the rightmost vertical stripe of 5s."""
    for c in range(grid.shape[1] - 1, -1, -1):
        if np.any(grid[:, c] == 5):
            return c
    return -1

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the horizontal gray lines
    gray_lines = find_horizontal_gray_lines(input_grid)
    if len(gray_lines) < 2:
        return output_grid  # Not enough gray lines for the transformation

    top_gray_line_row = gray_lines[0]
    bottom_gray_line_row = gray_lines[-1]

    # Find the rightmost vertical gray stripe
    rightmost_gray_stripe_col = find_rightmost_gray_stripe(input_grid)

    # Define source block dimensions.
    block_height = top_gray_line_row
    block_width = input_grid.shape[1] - (rightmost_gray_stripe_col + 1)
    
    # if there is nothing to copy - return input as output
    if block_width <=0 or block_height <= 0:
        return output_grid

    # Extract the source block.
    source_block = input_grid[0:block_height, rightmost_gray_stripe_col + 1:]

    # remove any columns that are all zeros from the source block
    non_zero_cols = np.any(source_block != 0, axis=0)
    source_block = source_block[:, non_zero_cols]
    
    # recalculate the width
    block_width = source_block.shape[1]

     # if there is nothing to copy - return input as output
    if block_width <=0:
        return output_grid
    
    # Determine how many times the block can be repeated
    available_height = output_grid.shape[0] - (bottom_gray_line_row + 1)
    num_repetitions = available_height // block_height

    # Copy and paste the source block repeatedly.
    for i in range(num_repetitions):
        start_row = bottom_gray_line_row + 1 + i * block_height
        end_row = start_row + block_height
        output_grid[start_row:end_row, rightmost_gray_stripe_col + 1:rightmost_gray_stripe_col+1+ block_width] = source_block

    return output_grid