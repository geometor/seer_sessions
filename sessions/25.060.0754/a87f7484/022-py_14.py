"""
The transformation rule is to crop the input grid to a 3x3 grid starting from the top-left corner.
"""

import numpy as np

def transform(input_grid):
    """
    Crops the input grid to a 3x3 subgrid from the top-left corner.
    """
    # Convert the input grid to a NumPy array.  This is a robust approach generally.
    input_array = np.array(input_grid)

    # Crop the array to 3x3, starting at [0,0].
    output_array = input_array[0:3, 0:3]

    # Convert the NumPy array back to a list of lists.  Technically the return
    # value does not need to match exactly, but doing this for consistency.
    output_grid = output_array.tolist()

    return output_grid