"""
The transformation rule involves identifying a single rectangular object of uniform color in the input grid. This rectangle is then replicated vertically. The replicated rectangle is appended below the original rectangle, doubling the height of the output grid while maintaining the original width. The color of the rectangle remains unchanged during the transformation.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by vertically replicating the single-color rectangle it contains.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid, which is the input grid replicated vertically.
    """
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)

    # Replicate the input array vertically.
    output_array = np.concatenate((input_array, input_array), axis=0)

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid