"""
The transformation rule is a 180-degree rotation of the input grid. This is equivalent to reversing the order of rows and then reversing the order of elements within each row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Convert the input list to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Reverse the order of rows (vertical flip)
    reversed_rows = np.flipud(input_array)

    # Reverse the order of elements in each row (horizontal flip)
    output_array = np.fliplr(reversed_rows)

    # Convert the NumPy array back to a list
    output_grid = output_array.tolist()

    return output_grid