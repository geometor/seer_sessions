"""
The input grid is vertically flipped to produce the output grid. The order of the rows is reversed while maintaining the cell values.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of its rows.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with rows in reversed order.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of rows using NumPy's flip function along the vertical axis (axis=0).
    output_array = np.flip(input_array, axis=0)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid