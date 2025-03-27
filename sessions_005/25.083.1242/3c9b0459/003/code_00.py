"""
The transformation rule is a 90-degree clockwise rotation of the input grid around its center. Each pixel in the input grid is moved to its new position as if the entire grid were rotated 90 degrees to the right.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by rotating it 90 degrees clockwise.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the rotated output grid.
    """
    # Convert the input list to a NumPy array
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees clockwise
    output_array = np.rot90(input_array, k=-1)  # k=-1 for 90-degree clockwise rotation

    # Convert the rotated array back to a list
    output_grid = output_array.tolist()

    return output_grid