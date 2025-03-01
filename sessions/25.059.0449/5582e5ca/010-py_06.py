"""
The transformation rule is to identify the presence of the digit '9' in the input grid and then create an output grid of the same dimensions, filling all cells with the digit '9'.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by filling a new grid of the same dimensions with the digit '9'.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid filled with '9'.
    """
    # Get the dimensions of the input grid.
    rows, cols = input_grid.shape

    # Create an output grid of the same dimensions, filled with '9'.
    output_grid = np.full((rows, cols), 9, dtype=int)

    return output_grid