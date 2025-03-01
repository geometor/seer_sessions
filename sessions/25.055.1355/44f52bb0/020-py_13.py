"""
Counts the number of red pixels (value 2) in the input grid.
Creates a 1x1 output grid.
If the count of red pixels is even, the output grid is filled with blue (1).
Otherwise the output is filled with black (0).
"""

import numpy as np

def transform(input_grid):
    # Count the number of red pixels (value 2)
    red_pixel_count = np.sum(input_grid == 2)

    # Create a 1x1 output grid
    output_grid = np.zeros((1, 1), dtype=int)

    # Fill the output grid based on the parity of the red pixel count
    if red_pixel_count % 2 == 0:
        output_grid[0, 0] = 1  # Blue
    else:
        output_grid[0, 0] = 0 # Black

    return output_grid