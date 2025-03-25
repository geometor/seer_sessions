"""
The transformation reverses the order of columns in the input 3x3 grid to produce the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms a 3x3 input grid by reversing the order of its columns.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of columns.
    output_array = input_array[:, ::-1]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid