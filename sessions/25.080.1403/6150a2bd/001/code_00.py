"""
The transformation is a 90-degree clockwise rotation of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The rotated output grid.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid.
    rows, cols = input_array.shape

    # Initialize the output grid with zeros.
    output_grid = np.zeros((cols, rows), dtype=int)

    # Perform the 90-degree clockwise rotation.
    for i in range(rows):
        for j in range(cols):
            output_grid[j][rows - 1 - i] = input_array[i][j]

    # Convert the output NumPy array back to a list of lists.
    return output_grid.tolist()