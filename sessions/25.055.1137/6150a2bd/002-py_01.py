"""
The input grid is rotated 90 degrees clockwise. The values from each cell maintain their identity, so the program is performing a grid rotation without any alteration of original values.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.
    
    Args:
        input_grid (list of lists): A 2D list representing the input grid.
    
    Returns:
        list of lists: The rotated grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    rotated_array = np.rot90(input_array, k=-1)

    # Convert the rotated array back to a list of lists
    output_grid = rotated_array.tolist()

    return output_grid