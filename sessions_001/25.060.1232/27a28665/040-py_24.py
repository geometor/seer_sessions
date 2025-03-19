"""
Determine the height of the input grid.
Create a 1x1 output grid.
Set the value of the single output pixel to be equal to the input grid height.
"""

import numpy as np

def transform(input_grid):
    """
    Calculates the height of the input and returns a 1x1 grid
    where the pixel's value is the height.
    """
    # Determine the height of the input grid.
    height = input_grid.shape[0]

    # Create a 1x1 output grid.
    output_grid = np.array([[height]])

    # The output grid is already set with the correct value.
    return output_grid