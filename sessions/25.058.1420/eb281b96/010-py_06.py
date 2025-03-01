"""
The transformation rule is to "double the input grid vertically," meaning
the output grid is created by stacking an exact copy of the input grid
below the original input grid. This is equivalent to vertical concatenation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by replicating it vertically (stacking a copy
    of the input grid below itself).

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed output grid.
    """
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Replicate the input grid vertically using concatenation
    output_grid = np.concatenate((input_grid, input_grid), axis=0)

    return output_grid