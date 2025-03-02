"""
The input, consisting of a single row of pixels, is replicated diagonally within a square output grid. The output grid's dimensions are determined by the input row's length, creating a square. Each row in the output is a copy of input. The placement is such that the copied rows form a diagonal line from the bottom-left corner to the top-right corner. The remaining cells in the output grid are filled with zeros (white).
"""

import numpy as np

def transform(input_grid):
    """Transforms a 1xN input grid into a NxN output grid by diagonally replicating the input.

    Args:
        input_grid: A numpy array representing the input grid (1xN).

    Returns:
        A numpy array representing the output grid.
    """
    input_length = input_grid.shape[1]
    output_size = input_length
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # Replicate the input row for each row of the output grid.
    for i in range(output_size):
        output_grid[i, :] = input_grid[0]

    return output_grid