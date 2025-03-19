"""
The transformation rule takes a 3x3 input grid and embeds it within a larger 9x9 output grid. The input grid is placed at the top-left corner of the output grid, and the rest of the output grid is filled with 0s (white).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by embedding it in a larger 9x9 grid.
    """
    # Initialize a 9x9 output grid filled with 0s.
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_height, input_width = input_grid.shape

    # Copy the input grid into the top-left corner of the output grid.
    output_grid[:input_height, :input_width] = input_grid

    return output_grid