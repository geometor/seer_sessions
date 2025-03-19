"""
Checks if the input grid contains any red pixels. If it does, creates a 1x3 output grid filled with red; otherwise, creates a 1x3 output grid filled with black.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid to output.
    """
    # Initialize output_grid as a 1x3 numpy array filled with zeros.
    output_grid = np.zeros((1, 3), dtype=int)

    # Check if any red pixels exist.
    input_grid_np = np.array(input_grid)
    red_exists = np.any(input_grid_np == 2)

    # If red pixels exist, fill the output grid with red (2).
    if red_exists:
        output_grid[:] = 2

    return output_grid.tolist()