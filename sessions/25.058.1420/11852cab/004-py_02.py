"""
The transformation rule is a horizontal reflection of specific rows. Non-white pixels on the second row are copied to the sixth row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by copying the non-white pixels from the second row to the sixth row.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Iterate through the pixels of the second row (index 1).
    for x in range(output_grid.shape[1]):
        # Check if the pixel is non-white (not 0).
        if output_grid[1, x] != 0:
            # Copy the pixel's value to the corresponding position in the sixth row (index 5).
            output_grid[5, x] = output_grid[1, x]

    return output_grid