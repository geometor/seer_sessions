"""
The transformation rule is as follows:
1. Change all values in the first row of the input grid from 3 to 5 (green to gray).
2. Change all values in the remaining rows (second and third rows) from 3 to 0 (green to white).
3. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.  We'll modify it directly.
    output_grid = np.copy(input_grid)
    
    # Change the first row to 5 (gray).
    output_grid[0, :] = 5
    
    # Change the remaining rows to 0 (white).
    output_grid[1:, :] = 0
    
    return output_grid