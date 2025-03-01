"""
The input grid consists of a single, large gray rectangle filling the entire grid.
A new row of blue pixels is added to the bottom of the grid. The height of the
output grid increases by one, and its width stays the same.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by adding a blue row at the bottom.
    """
    # Get the dimensions of the input grid.
    height, width = input_grid.shape

    # Create a new row of blue pixels.  The color blue is represented by 1.
    new_row = np.full((1, width), 1)

    # Concatenate the input grid with the new row vertically (along axis 0).
    output_grid = np.concatenate((input_grid, new_row), axis=0)

    return output_grid