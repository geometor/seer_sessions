"""
The transformation rule checks for the presence of the digit '9' (maroon) in the input grid. If '9' is present, the output grid is filled with '9's, maintaining the same dimensions as the input. If '9' is not present, the output grid is filled with '0's, also maintaining the same dimensions.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of the digit '9'.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Check if the value '9' is present in the input grid.
    if 9 in input_grid:
        # If '9' is present, create an output grid of the same dimensions filled with '9'.
        output_grid = np.full(input_grid.shape, 9, dtype=int)
    else:
        # If '9' is not present, create an output grid of the same dimensions filled with '0'.
        output_grid = np.full(input_grid.shape, 0, dtype=int)

    return output_grid