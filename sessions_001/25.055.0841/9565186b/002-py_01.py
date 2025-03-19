"""
Replace blue and azure pixels with gray pixels, leaving red pixels unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid

    # Iterate through each pixel of the grid
    for row_index, row in enumerate(input_grid):
        for col_index, pixel_value in enumerate(row):
            # Change output pixels: Check if the pixel is blue (1) or azure (8)
            if pixel_value == 1 or pixel_value == 8:
                output_grid[row_index, col_index] = 5  # Change to gray (5)

    return output_grid