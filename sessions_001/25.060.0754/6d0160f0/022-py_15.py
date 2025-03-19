"""
The transformation preserves all horizontally contiguous sequences of gray (5) pixels and converts all other pixels to white (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid, filled with 0s.
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each row and column of the input grid.
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is gray (5).
            if input_grid[r, c] == 5:
                # If it's a 5, preserve it in the output grid.
                output_grid[r, c] = 5
            # else the output grid is already initialized to 0 so do nothing

    return output_grid