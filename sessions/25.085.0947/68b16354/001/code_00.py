"""
Reverses the order of the rows in the input grid to produce the output grid.
This is equivalent to a vertical flip or reflection across the horizontal midline.
"""

import numpy as np

def transform(input_grid):
    """
    Reverses the order of the rows in the input grid.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The output grid with rows reversed.
    """
    # Convert the input list of lists to a NumPy array for efficient slicing
    input_array = np.array(input_grid, dtype=int)

    # Reverse the order of the rows using slicing
    # [::-1] creates a reversed view of the rows along the first axis (axis 0)
    output_array = input_array[::-1, :]

    # Convert the NumPy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid
