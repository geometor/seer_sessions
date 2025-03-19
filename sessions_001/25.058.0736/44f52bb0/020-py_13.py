"""
Counts non-black colored pixels in the input grid.
If there are exactly two such pixels, the output is a 1x1 blue (1) grid.
Otherwise, the output is a 1x1 black (0) grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid to a 1x1 black grid.
    output_grid = np.array([[0]])

    # Count non-black pixels.
    non_black_pixel_count = np.count_nonzero(input_grid)

    # Check if the count of non-black pixels is exactly 2.
    if non_black_pixel_count == 2:
        output_grid = np.array([[1]])

    return output_grid