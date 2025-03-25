"""
Constructs a 2x2 output grid by selecting specific pixels from the top-left and bottom-right corners of the input grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Initialize the output grid
    output_grid = np.zeros((2, 2), dtype=int)

    # Select pixels from the corners
    output_grid[0, 0] = grid[0, 0]  # Top-left
    output_grid[0, 1] = grid[0, 1]  # Top-left

    if rows % 2 == 1: # if odd
      output_grid[1, 0] = grid[rows - 2, cols - 2] # Bottom Right, skip center
      output_grid[1, 1] = grid[rows - 1, cols - 1]
    else:
      output_grid[1, 0] = grid[rows - 2, cols - 2]
      output_grid[1, 1] = grid[rows - 1, cols - 1]

    return output_grid.tolist()