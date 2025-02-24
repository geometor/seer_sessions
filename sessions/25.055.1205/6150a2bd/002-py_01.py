"""
Rotate the input grid by 180 degrees around its center.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the grid by 180 degrees.  NumPy's rot90 function rotates by 90
    # degrees counter-clockwise, so we call it twice.
    output_array = np.rot90(input_array, 2)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()
    return output_grid