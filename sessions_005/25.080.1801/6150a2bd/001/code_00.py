"""
Rotate the input grid 90 degrees clockwise and reverse the order of the rows.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise and reverses the order of rows.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Reverse the order of the rows
    reversed_array = np.flip(rotated_array, axis=0)
    
    # Convert the NumPy array back to a list of lists
    output_grid = reversed_array.tolist()

    return output_grid