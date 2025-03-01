"""
1. Change all white (0) pixels in the input grid to azure (8) in the output grid.
2. Identify the locations of all blue (1) pixels in the input grid.
3. Copy all blue pixels to same location in output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Change all white (0) pixels to azure (8)
    output_grid[output_grid == 0] = 8

    # Find the locations of all blue (1) pixels in the input grid.
    blue_pixel_locations = np.where(input_grid == 1)

    # Copy blue pixels to same location in output grid.
    output_grid[blue_pixel_locations] = 1
    
    return output_grid