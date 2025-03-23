"""
The transformation flips the input grid both horizontally and vertically. It can be thought of as a 180-degree rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of elements in each row and then
    reversing the order of the rows.  This is equivalent to a 180-degree rotation.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse each row.
    reversed_rows = [row[::-1] for row in input_array]

    # Reverse the order of the rows.
    output_array = reversed_rows[::-1]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid