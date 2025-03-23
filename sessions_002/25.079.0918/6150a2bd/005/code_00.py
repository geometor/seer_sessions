"""
The transformation rule is a 90-degree counter-clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the rotated grid.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)
    rows = input_array.shape[0]
    cols = input_array.shape[1]

    # Initialize the output array with the correct dimensions.
    output_array = np.empty((cols, rows), dtype=int)

    # Iterate through the input grid and calculate the new position of each pixel.
    for x in range(rows):
        for y in range(cols):
            output_array[y, rows - 1 - x] = input_array[x, y]

    # Convert the result back to a list.
    output_grid = output_array.tolist()

    return output_grid