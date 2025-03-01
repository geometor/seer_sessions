"""
The output is always a 1x1 grid. If the input grid contains at least one red pixel, the output grid is a single blue pixel. If the input grid contains no red pixels, the output grid is a single white pixel.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 1x1 grid.
    output_grid = np.zeros((1, 1), dtype=int)

    # Check if the input grid contains any red pixels (value 2).
    has_red = np.any(input_grid == 2)

    # Set the output pixel based on the presence of red.
    if has_red:
        output_grid[0, 0] = 1  # Blue pixel
    else:
        output_grid[0, 0] = 0  # White pixel

    return output_grid