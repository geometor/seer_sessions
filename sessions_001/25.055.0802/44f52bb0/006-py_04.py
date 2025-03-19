"""
Examine the input grid for the presence of any non-zero pixels.
If any non-zero pixels are found, the output is a 1x1 grid with a blue pixel (1).
If the grid is entirely white (0), the output is a 1x1 grid with a white pixel (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Check for the presence of any non-zero pixels.
    non_zero_pixels = input_array[input_array != 0]

    # Create the output grid based on the presence of non-zero pixels.
    if non_zero_pixels.size > 0:
        output_grid = [[1]]  # Output a 1x1 grid with a blue pixel (1).
    else:
        output_grid = [[0]]  # Output a 1x1 grid with a white pixel (0).

    return output_grid