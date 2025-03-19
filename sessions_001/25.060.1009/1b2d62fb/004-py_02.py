"""
Identify the central, vertical blue stripe in the input grid. Extract the bottom two pixels of the blue stripe. Change the color of these pixels to azure. Create a new 5x3 grid, filling it with white (0) except for the two adjacent azure pixels which correspond to the transformed bottom part of the blue stripe.
"""

import numpy as np

def find_blue_stripe(grid):
    # Find the column index where the blue stripe (color 1) exists. Assumes one continuous stripe.
    rows, cols = grid.shape
    for j in range(cols):
        if np.any(grid[:, j] == 1):
            return j
    return -1  # No blue stripe found

def transform(input_grid):
    # Initialize output_grid as 5x3, filled with white (0)
    output_grid = np.zeros((5, 3), dtype=int)

    # Find the central blue stripe column
    stripe_col = find_blue_stripe(input_grid)

    # If a blue stripe is found...
    if stripe_col != -1:
        # Find the indices of blue pixels in the stripe column
        blue_indices = np.where(input_grid[:, stripe_col] == 1)[0]

        # Check if we have at least two blue pixels
        if len(blue_indices) >= 2:
            # Get the bottom two blue pixels
            #output_grid[3, 1] = 8  # bottom 2
            #output_grid[3, 2] = 8
            output_grid[3, stripe_col % 3] = 8
            output_grid[3, (stripe_col+1) % 3 ] = 8

    return output_grid