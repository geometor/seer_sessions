"""
The input grid is mirrored both horizontally and vertically to produce the output grid. The output grid's dimensions are double that of the input grid in both height and width.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by mirroring it horizontally and vertically.
    """
    # Create a numpy array from the input grid
    input_array = np.array(input_grid)

    # Reflect the input array horizontally
    horizontal_reflection = np.fliplr(input_array)

    # Concatenate the original and reflected arrays horizontally
    top_half = np.concatenate((input_array, horizontal_reflection), axis=1)

    # Reflect the top half vertically
    bottom_half = np.flipud(top_half)

    # Concatenate the top and bottom halves vertically
    output_array = np.concatenate((top_half, bottom_half), axis=0)

    # Convert the numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid