"""
Copy rows 0-3 of the input grid to rows 11-14 of the output grid.
Copy row 15 of the input grid to row 15 of the output grid.
Fill row 10 of the output grid with azure (color 8).
Fill the remaining cells of the output grid with black (color 0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with all zeros (black).
    output_grid = np.zeros_like(input_grid)

    # Copy rows 0-3 to rows 11-14.
    for i in range(4):
        if i < input_grid.shape[0]:  # Handle cases where input might be smaller than expected
           output_grid[11 + i, :] = input_grid[i, :]

    # Copy row 15 to row 15.
    if 15 < input_grid.shape[0]: # Handle cases where input might be smaller than expected
        output_grid[15, :] = input_grid[15, :]

    # Fill row 10 with azure.
    output_grid[10, :] = 8

    return output_grid