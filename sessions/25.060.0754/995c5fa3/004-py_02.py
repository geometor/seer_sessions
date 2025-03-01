"""
The transformation rule is to create a 3x3 grid where the top row is red (2), the middle row is azure (8), and the bottom row is green (3), regardless of the input.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 3x3 output grid.
    output_grid = np.zeros((3, 3), dtype=int)

    # Set the top row to red (2).
    output_grid[0, :] = 2

    # Set the middle row to azure (8).
    output_grid[1, :] = 8

    # Set the bottom row to green (3).
    output_grid[2, :] = 3

    return output_grid