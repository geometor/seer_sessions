"""
Reflects a 3x3 grid along its top-right to bottom-left diagonal.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reflecting it along the top-right to
    bottom-left diagonal.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Initialize the output grid as a copy of the input array
    output_array = np.copy(input_array)
    
    # Get the height and width of the input grid
    height, width = np.shape(input_grid)

    # Reflect the grid by exchanging elements along anti-diagonal.
    for i in range(height):
        for j in range(width):
            output_array[i, j] = input_array[j, i]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid