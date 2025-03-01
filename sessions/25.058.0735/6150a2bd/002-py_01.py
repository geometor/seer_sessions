"""
The transformation rule is a 180-degree rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array by 180 degrees.  NumPy's rot90 function rotates by 90 degrees,
    # so we call it twice.
    output_array = np.rot90(input_array, 2)

    # Convert the rotated array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid