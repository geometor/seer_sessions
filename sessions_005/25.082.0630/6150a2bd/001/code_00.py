"""
The input grid is transformed to the output grid by reversing the order of its rows and columns. This is equivalent to a 180-degree rotation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by reversing the order of its rows and columns.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Reverse the order of rows.
    reversed_rows = np.flipud(input_array)

    # Reverse the order of columns.
    output_array = np.fliplr(reversed_rows)
    
    # Convert the NumPy array back to a 2D list.
    output_grid = output_array.tolist()

    return output_grid