"""
1. Copy: Create a copy of the input grid and call it the output grid.
2. Check for Blue: Examine the input grid. If there are any blue pixels (pixels with a value of 1), proceed to the next step.
3. Paint Red: Replace the pixel at coordinates (0, 0) in the *output* grid with a red pixel (value 2). If there are no blue pixels, the output grid remains identical to the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Check for Blue: If there is any blue pixel
    if np.any(input_grid == 1):
        # Paint Red: paint one red pixel at (0,0)
        output_grid[0, 0] = 2

    return output_grid