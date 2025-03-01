"""
Interleaves the colors of two input rows to create a checkerboard pattern in a 2x6 grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 2x6 input grid with two rows of uniform colors into a 2x6 output
    grid with an interleaved checkerboard pattern.

    Args:
        input_grid: A 2x6 NumPy array representing the input grid.

    Returns:
        A 2x6 NumPy array representing the output grid with the interleaved
        checkerboard pattern.
    """
    # Get the colors from the two rows.
    color_1 = input_grid[0, 0]
    color_2 = input_grid[1, 0]

    # Initialize the output grid.
    output_grid = np.zeros_like(input_grid)

    # Create the interleaved pattern for the first row.
    output_grid[0, ::2] = color_1
    output_grid[0, 1::2] = color_2

    # Create the interleaved pattern for the second row.
    output_grid[1, ::2] = color_2
    output_grid[1, 1::2] = color_1

    return output_grid