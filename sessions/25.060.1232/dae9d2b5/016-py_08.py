"""
The transformation rule is as follows:
1. Create an output grid of dimensions 3x3.
2. Keep the pixel at coordinates (0, 0) the same in the output.
3. Iterate through all other pixels in the output grid. If there is a corresponding non-zero pixel at the input index, change the output pixel to magenta (6).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as 3x3 filled with magenta (6)
    output_grid = np.full((3, 3), 6)

    # Copy input grid first element to output grid
    output_grid[0, 0] = input_grid[0, 0]

    # All other output grid index will be 6

    return output_grid