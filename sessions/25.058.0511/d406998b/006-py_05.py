"""
Iterate through all gray pixels in row-major order (left-to-right, top-to-bottom). For every group of three consecutive gray pixels, change the third one to green.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # Find the positions of all '5' (gray) pixels
    gray_positions = np.argwhere(input_grid == 5)
    
    # Counter for the pattern (keep 2, change 1)
    count = 0
    
    # Iterate through the positions and apply the transformation
    for pos in gray_positions:
        if count < 2:
            count += 1
        else:
            output_grid[pos[0], pos[1]] = 3  # Change to green
            count = 0

    return output_grid