"""
The output grid is a 3x3 subgrid extracted from the input grid. The subgrid
consists of the uppermost and leftmost pixels of the input grid. If the input
grid is smaller than 3x3, the available pixels are used, and the output will
be smaller than 3x3. The function takes the largest possible subgrid up to 3x3.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the largest possible subgrid (up to 3x3) from the top-left corner
    of the input grid.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The extracted subgrid.
    """
    # Determine the dimensions of the subgrid.
    rows = min(3, input_grid.shape[0])
    cols = min(3, input_grid.shape[1])

    # Extract the subgrid.
    output_grid = input_grid[:rows, :cols].copy()

    return output_grid