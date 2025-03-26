"""
Takes an input grid and duplicates it horizontally to create the output grid.
The output grid has the same height as the input grid but twice the width.
The left half of the output grid is identical to the input grid, and the right
half is also identical to the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Duplicates the input grid horizontally.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The output grid, which is the input grid concatenated
                     horizontally with itself.
    """
    # Convert input_grid to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Get the dimensions of the input grid
    height, width = input_np.shape

    # Create the output grid by horizontally stacking the input grid with itself
    # np.hstack concatenates arrays along the second axis (columns)
    output_grid = np.hstack((input_np, input_np))

    return output_grid
