"""
1. Identify: Locate all pixels in the input grid that are either blue (1) or azure (8).
2. Transform: Change the color of all identified pixels (blue and azure) to gray (5).
3. Preserve: Leave all other pixels (red (2)) unchanged.
4. Output: Present the modified grid as the output.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid to preserve unchanged pixels.
    output_grid = np.copy(input_grid)

    # Iterate through each pixel of the grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Change output pixels: Check if the pixel is blue (1) or azure (8)
            if output_grid[i, j] == 1 or output_grid[i, j] == 8:
                # Transform the pixel to gray (5)
                output_grid[i, j] = 5

    return output_grid