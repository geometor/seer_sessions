"""
Takes an input grid and duplicates it horizontally, placing the copy immediately to the right of the original, resulting in an output grid with the same height but double the width.
"""

import numpy as np

def transform(input_grid):
    """
    Duplicates the input grid horizontally.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The output grid containing two copies of the input grid
                     placed side-by-side.
    """
    # Convert input grid to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Concatenate the input array with itself along the horizontal axis (axis=1)
    # This effectively places a copy of the input array to the right of the original
    output_grid = np.concatenate((input_array, input_array), axis=1)

    # Return the resulting grid
    return output_grid
