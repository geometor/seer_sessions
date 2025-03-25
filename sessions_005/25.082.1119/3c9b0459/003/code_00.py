"""
Reverse the order of rows in a grid.
"""

import numpy as np

def transform(input_grid):
    """
    Reverses the order of rows in a grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of rows using NumPy's array slicing.
    output_array = input_array[::-1]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    # Return the modified grid
    return output_grid