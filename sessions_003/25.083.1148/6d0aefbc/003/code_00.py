"""
The input grid is transformed into an output grid with twice the number of columns. Each column in the input
grid appears twice in the output grid. The order of columns is a reversed duplication.  For example,
if input columns are [A, B, C], output columns are [A, B, C, C, B, A].
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating and reversing its columns.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols * 2), dtype=int)

    # Copy original columns
    for j in range(cols):
        output_grid[:, j] = input_grid[:, j]

    # Copy reversed columns
    for j in range(cols):
        output_grid[:, 2 * cols - 1 - j] = input_grid[:, j]

    return output_grid.tolist()