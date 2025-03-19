"""
Counts the number of blue (1) pixels in the input grid and creates a 1xN output grid filled with blue pixels, where N is the count of blue pixels in the input.
"""

import numpy as np

def transform(input_grid):
    # Count the number of blue (1) pixels in the input grid.
    blue_count = np.sum(input_grid == 1)

    # Create a new grid with dimensions 1xN, where N is the blue_count.
    output_grid = np.ones((1, blue_count), dtype=int)

    return output_grid