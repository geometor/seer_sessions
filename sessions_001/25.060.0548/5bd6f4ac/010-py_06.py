"""
1. **Identify Target Elements:** Examine the input grid. Select the elements from the second row with positions within columns 7-9 and construct the new grid.
2. **Construct output:** The selected numbers forms a new grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Select elements from the input_grid (second row, columns 7-9).
    output_grid[0,0] = input_grid[0,7]
    output_grid[0,1] = input_grid[0,8]
    output_grid[0,2] = input_grid[0,9]
    output_grid[1,0] = input_grid[1,7]
    output_grid[1,1] = input_grid[1,8]
    output_grid[1,2] = input_grid[1,9]
    output_grid[2,0] = input_grid[2,7]
    output_grid[2,1] = input_grid[2,8]
    output_grid[2,2] = input_grid[2,9]
   

    return output_grid