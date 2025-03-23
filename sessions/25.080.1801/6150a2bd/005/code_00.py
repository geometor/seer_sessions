"""
Rotate the input grid 90 degrees clockwise and then reflect across both x and y axis.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise and reflects it across x and y axis.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Reflect across x axis (flip vertically)
    reflected_x = np.flip(rotated_array, axis=0)

    # Reflect across y axis (flip horizontally)
    reflected_xy = np.flip(reflected_x, axis=1)
    
    # Convert the NumPy array back to a list of lists
    output_grid = reflected_xy.tolist()

    return output_grid