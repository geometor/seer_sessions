"""
The input grid is rotated 90 degrees counter-clockwise. The values of the grid elements (representing colors) are maintained, but their positions within the grid are updated based on the rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array, k=1)  # k=1 for 90-degree counter-clockwise

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid