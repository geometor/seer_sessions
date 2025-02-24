"""
The input grid is transformed by changing the value of the top-center cell to white (0) if the input grid has an odd number of columns. The rest of the grid remains unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # check if the number of columns is odd
    if output_grid.shape[1] % 2 != 0:
        # find the center column index
        center_col = output_grid.shape[1] // 2
        # change the top-center cell to white (0)
        output_grid[0, center_col] = 0

    return output_grid