"""
Copy the input grid. Find a vertical line through the center. Replace the white pixels in the line with Red.
"""

import numpy as np

def find_vertical_center_line(grid):
    """
    Finds the center column index of the grid.
    """
    _, num_cols = grid.shape
    center_col = num_cols // 2
    return center_col

def transform(input_grid):
    """
    Transforms the input grid by replacing white pixels on a center vertical line with red pixels.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the center column index
    center_col = find_vertical_center_line(output_grid)

    # Iterate and replace white pixels with red along the center line.
    for r in range(rows):
            if output_grid[r, center_col] == 0:
                output_grid[r, center_col] = 2

    return output_grid