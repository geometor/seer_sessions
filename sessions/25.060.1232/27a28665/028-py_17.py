"""
The transformation rule depends on the presence of azure (8) pixels in the input grid. If azure pixels are present, the output is a 1x1 grid containing the count of azure pixels. If no azure pixels are present, the output is a 1x1 grid containing the value 0.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the presence of azure pixels.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: A 1x1 grid containing the count of azure pixels or 0.
    """
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Count all azure pixels
    azure_count = np.count_nonzero(input_array == 8)

    # Create the 1x1 output grid based on the presence of azure pixels.
    if azure_count > 0:
        output_grid = [[azure_count]]
    else:
        output_grid = [[0]]

    return output_grid