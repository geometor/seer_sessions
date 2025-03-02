"""
The transformation rule is as follows:
1. The output grid is always 3x3.
2. The color of the pixels in the output grid corresponds to the color of the pixels at the same position in the input grid.
3. If the input grid is smaller than 3x3, any missing pixels are treated as having color 6 (magenta).
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as 3x3 filled with magenta (6)
    output_grid = np.full((3, 3), 6)

    # Iterate through the input grid and copy corresponding pixel values to the output grid
    for i in range(min(input_grid.shape[0], 3)):
        for j in range(min(input_grid.shape[1], 3)):
            output_grid[i, j] = input_grid[i, j]

    return output_grid