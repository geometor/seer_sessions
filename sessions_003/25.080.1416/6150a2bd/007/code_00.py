"""
The transformation rule is a combination of two operations:
1. Transpose the input grid.
2. Reflect the transposed grid vertically.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by first transposing it and then reflecting it vertically.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Transpose the array.
    transposed_array = np.transpose(input_array)

    # Reflect the transposed array vertically.
    reflected_array = np.flip(transposed_array, axis=0)

    # Convert the reflected array back to a list of lists.
    output_grid = reflected_array.tolist()

    return output_grid