"""
Extracts the right-most blue (1), red (2), and yellow (4) columns from the input grid, ignoring white (0) and gray (5), and constructs a 3x3 output grid representing these columns.
"""

import numpy as np

def get_target_columns(input_grid):
    """Find right-most occurrence of target colors (1,2,4) in input_grid columns"""
    target_colors = [1, 2, 4]
    target_columns_values = []
    
    for j in range(input_grid.shape[1]): # iterate columns
        column = input_grid[:, j]
        target_pixels = [val for val in column if val in target_colors]

        if target_pixels: # found a target color in the column
            target_columns_values.append(target_pixels[-1])  # save last occurrence, right-most from original

    return target_columns_values
            

def transform(input_grid):
    # initialize output_grid
    target_columns_values = get_target_columns(input_grid)

    # handle edge case: fewer than 3 target columns
    while len(target_columns_values) < 3:
        target_columns_values.append(0) # append background if needed
    # handle edge case: more than 3 target columns
    if len(target_columns_values) > 3:
        target_columns_values = target_columns_values[:3] # keep first 3

    output_grid = np.array([target_columns_values, target_columns_values, target_columns_values])

    return output_grid