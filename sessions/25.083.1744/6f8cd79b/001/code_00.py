"""
The function transforms a grid of black (0) pixels into a grid with an azure (8) border. The interior pixels remain black.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a grid of 0s to have a border of 8s.
    """
    # Create output grid with same dimensions.
    output_grid = np.zeros_like(input_grid)
    height, width = input_grid.shape

    # Iterate through output grid and modify the boundary
    for row_index in range(height):
        for col_index in range(width):
            # Check if the cell is at the boundary
            if row_index == 0 or col_index == 0 or row_index == height - 1 or col_index == width -1:
                output_grid[row_index, col_index] = 8  #set to color 8
            else:
                output_grid[row_index, col_index] = 0 #maintain color 0

    return output_grid