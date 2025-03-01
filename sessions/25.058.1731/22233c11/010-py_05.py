"""
Copy the input grid to the output grid. Then, add two azure (8) pixels to the top-left corner and two azure pixels to the bottom-right corner of the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)  # Copy the input grid

    # Add azure pixels to the top-left corner
    output_grid[1, 0] = 8
    output_grid[2, 0] = 8

    # Add azure pixels to the bottom-right corner
    output_grid[7, 5] = 8
    output_grid[8, 5] = 8

    return output_grid