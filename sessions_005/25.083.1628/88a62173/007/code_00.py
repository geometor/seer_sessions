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

    # Top-left
    output_grid[0, 0] = grid[0, 0]

    # Top-right
    output_grid[0, 1] = grid[0, 1]

    # Bottom-right
    output_grid[1, 1] = grid[rows - 1, cols - 1]
    
    # Bottom-left
    output_grid[1, 0] = grid[rows-2, cols-2]


    return output_grid.tolist()