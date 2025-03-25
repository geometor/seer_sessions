"""
The input grid is transformed into an output grid where each pixel in the input is replaced by a 2x2 block of the same color in the output. This effectively doubles the dimensions of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by expanding each pixel into a 2x2 block of the same color.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The expanded output grid.
    """
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    output_array = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Iterate through each pixel in the input grid
    for i in range(rows):
        for j in range(cols):
            # Replicate the pixel's value into a 2x2 block in the output grid
            output_array[2*i:2*i+2, 2*j:2*j+2] = input_array[i, j]

    return output_array.tolist()