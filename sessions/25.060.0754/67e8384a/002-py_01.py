"""
The input grid (3x3) is transformed into a larger output grid (6x6). Each pixel in the input grid is replicated in a 2x2 block in the output grid, forming a symmetrical cross-like shape.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid into a 6x6 output grid by replicating each pixel in a 2x2 block.

    Args:
        input_grid: A 3x3 numpy array representing the input grid.

    Returns:
        A 6x6 numpy array representing the output grid.
    """
    # Initialize the output grid with dimensions twice the size of the input grid.
    output_grid = np.zeros((6, 6), dtype=int)

    # Iterate through each pixel of the input grid.
    for row in range(3):
        for col in range(3):
            # Replicate the pixel's value to a 2x2 block in the output grid.
            value = input_grid[row, col]
            output_grid[2 * row, 2 * col] = value
            output_grid[2 * row + 1, 2 * col] = value
            output_grid[2 * row, 2 * col + 1] = value
            output_grid[2 * row + 1, 2 * col + 1] = value

    return output_grid