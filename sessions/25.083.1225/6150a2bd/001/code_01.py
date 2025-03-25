"""
The transformation is a 180-degree rotation of the entire grid (or equivalently, a horizontal flip followed by a vertical flip).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 180 degrees.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Convert the input list of lists to a NumPy array
    input_array = np.array(input_grid)

    # Reverse the order of rows (vertical flip)
    output_array = np.flipud(input_array)

    # Reverse the order of elements in each row (horizontal flip)
    output_array = np.fliplr(output_array)

    # return the transformed array
    return output_array.tolist()