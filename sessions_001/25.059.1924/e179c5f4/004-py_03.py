"""
Transforms an input grid containing a single blue (1) pixel among white (0) pixels into an output grid of the same dimensions. The output grid replaces the white pixels with an alternating pattern of azure (8) and blue (1) pixels. The starting value (8 or 1) of the alternating pattern in each row is determined by the column index of the blue pixel in the input grid.
"""

import numpy as np

def find_blue_pixel(grid):
    # Find the coordinates of the blue pixel (value 1).
    for r_idx, row in enumerate(grid):
        for c_idx, val in enumerate(row):
            if val == 1:
                return (r_idx, c_idx)
    return None  # Should not happen in this specific task, but good practice.

def transform(input_grid):
    """
    Transforms the input grid as per the described rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output grid with the same dimensions.
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Locate the blue pixel in the input grid.
    blue_row, blue_col = find_blue_pixel(input_grid)

    # Populate the output grid.
    for r_idx in range(height):
        # Determine the starting value for the alternating pattern.
        if (blue_col + r_idx) % 2 == 0:
            start_val = 8
        else:
            start_val = 1

        # Fill the row with the alternating pattern.
        for c_idx in range(width):
            if (c_idx % 2) == 0:
               output_grid[r_idx, c_idx] = start_val
            elif start_val == 8:
                output_grid[r_idx, c_idx] = 1
            else:
                output_grid[r_idx,c_idx] = 8

    return output_grid