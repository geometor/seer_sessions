"""
Counts the number of red pixels in the input grid and represents that count as a single pixel in a 1x1 grid.
"""

import numpy as np

def transform(input_grid):
    # Count the number of red pixels (value 2) in the input grid.
    red_pixel_count = np.sum(input_grid == 2)

    # Create a 1x1 output grid.
    output_grid = np.zeros((1, 1), dtype=int)

    # Set the value of the output pixel to the count of red pixels.
    output_grid[0, 0] = red_pixel_count

    return output_grid