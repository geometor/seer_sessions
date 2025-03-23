"""
Transforms the input grid by rotating it 180 degrees.
This is equivalent to reversing the order of rows and then reversing the order of elements within each row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by rotating it 180 degrees.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation
    input_array = np.array(input_grid)

    # Reverse the order of rows (vertical flip)
    flipped_vertical = np.flipud(input_array)

    # Reverse the order of elements within each row (horizontal flip)
    rotated_array = np.fliplr(flipped_vertical)
    
    # Convert the NumPy array back to a list
    output_grid = rotated_array.tolist()

    return output_grid