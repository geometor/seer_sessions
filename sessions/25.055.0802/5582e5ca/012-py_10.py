"""
The transformation rule involves replacing all pixels in the input grid with the color maroon (digit 9). The output grid maintains the same dimensions as the input grid, but every cell's value is changed to 9, regardless of its original value.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to preserve original dimensions.
    output_grid = np.copy(input_grid)

    # Set all pixel values in the output grid to 9 (maroon).
    output_grid[:] = 9

    return output_grid