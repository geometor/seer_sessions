"""
Iterate through each pixel in the input grid. Keep white pixels. For non-white pixels, check neighbors. If both neighbors are white, change the pixel to white; otherwise, keep its original color.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with the same dimensions and data type as the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for i in range(rows):
        for j in range(cols):
            # Keep white pixels
            if input_grid[i, j] == 0:
                continue

            # Check neighbors for non-white pixels
            left_neighbor = 0 if j == 0 else input_grid[i, j - 1]
            right_neighbor = 0 if j == cols - 1 else input_grid[i, j + 1]

            # If both neighbors are white, change the pixel to white
            if left_neighbor == 0 and right_neighbor == 0:
                output_grid[i, j] = 0
            # Otherwise (if at least one neighbor is the same color), keep original color - implicit because we initialized to input

    return output_grid