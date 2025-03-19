"""
The transformation rule is a cyclical color substitution.  Specifically:

1.  All pixels with the color value 1 (blue) are changed to color value 2 (red).
2.  All pixels with the color value 2 (red) are changed to color value 3 (green).
3.  All pixels with the color value 3 (green) are changed to color value 1 (blue).
4.  Pixels with any other color value remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each pixel in the grid
    for row_index, row in enumerate(output_grid):
        for col_index, pixel_value in enumerate(row):
            # Apply the color substitution rules
            if pixel_value == 1:
                output_grid[row_index, col_index] = 2
            elif pixel_value == 2:
                output_grid[row_index, col_index] = 3
            elif pixel_value == 3:
                output_grid[row_index, col_index] = 1

    return output_grid