"""
The transformation rule extracts the two rightmost columns of the input grid and uses them to form the output grid. The relative positions and values of the pixels in these two columns are preserved.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the two rightmost columns of the input grid to form the output grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The output grid, which consists of the two rightmost columns of the input grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_array = np.array(input_grid)

    # Get the height and width of the input grid
    height, width = input_array.shape

    # Extract the two rightmost columns
    output_array = input_array[:, width-2:width]

    # Convert the output array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid