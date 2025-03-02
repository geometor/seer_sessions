"""
1. Copy: Copy the input grid to the output grid
2. Check for Blue: Examine the input grid. If there are any blue pixels (pixels with a value of 1), proceed to the next step.
3. Paint Red: Create one red pixel at the coordinates (0, 0) in the output grid, regardless all blue pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Check for Blue: If there is any blue pixel
    if np.any(input_grid == 1):
        # Paint Red: paint one red pixel
        output_grid[0, 0] = 2

    return output_grid