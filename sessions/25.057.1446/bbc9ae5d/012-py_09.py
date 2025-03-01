"""
The transformation rule takes a 1xN input grid and generates a 1xN output grid. All red (2) pixels in the input are moved to the beginning of the output row, forming a contiguous block. The remaining cells in the output row are filled with white (0) pixels.
"""

import numpy as np

def transform(input_grid):
    # Count the number of red pixels in the input grid.
    red_count = np.sum(input_grid == 2)

    # Create a new output grid with the same dimensions as the input grid.
    output_grid = np.zeros_like(input_grid)

    # Place the red pixels at the beginning of the output row.
    output_grid[0, :red_count] = 2

    # Fill the remaining cells with white (0) pixels.
    # output_grid[0, red_count:] = 0  # This line is redundant, as the grid is initialized with 0s.

    return output_grid