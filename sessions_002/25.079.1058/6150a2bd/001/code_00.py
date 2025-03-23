"""
The input grid is transposed and then each row of the transposed grid is reversed.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by transposing it and then reversing each row.

    Args:
        input_grid: A 2D list representing the input grid.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Transpose the input grid using numpy
    transposed_grid = np.array(input_grid).T.tolist()

    # Initialize the output grid
    output_grid = []

    # Reverse each row in the transposed grid
    for row in transposed_grid:
        output_grid.append(row[::-1])

    return output_grid