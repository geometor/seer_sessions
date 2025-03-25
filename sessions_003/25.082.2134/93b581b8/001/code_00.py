"""
The transformation rule involves identifying the two center columns of the input grid, mirroring them to the left and right sides,
and then inverting the order of mirrored columns.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    # Initialize output grid with the same dimensions as the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify the two center columns
    center_col1 = cols // 2 -1
    center_col2 = cols // 2

    # Mirror the second central column to the two leftmost columns
    output_grid[:, 0] = input_grid[:, center_col2]
    output_grid[:, 1] = input_grid[:, center_col2]

    # Mirror the first center column to the rightmost columns
    output_grid[:, cols - 2] = input_grid[:, center_col1]
    output_grid[:, cols - 1] = input_grid[:, center_col1]

    return output_grid