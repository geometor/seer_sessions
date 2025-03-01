"""
The transformation rule checks for the presence of gray pixels (value 5) in the input grid. If gray pixels are present, and their count is odd, the output is a 1x1 grid containing the value 1. Otherwise (no gray pixels, or an even count of gray pixels), the output is a 1x1 grid containing the value 0.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 1x1 numpy array with a default value of 0.
    output_grid = np.array([[0]])

    # Count the number of gray pixels.
    gray_count = np.sum(input_grid == 5)

    # If gray pixels are present and their count is odd, change the output to 1.
    if gray_count > 0 and gray_count % 2 != 0:
        output_grid[0, 0] = 1

    return output_grid