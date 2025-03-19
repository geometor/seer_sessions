"""
The input grid is mirrored vertically (top-to-bottom).  This is achieved by swapping each row with its mirrored counterpart: row 0 swaps with row n-1, row 1 swaps with row n-2, and so on, where n is the total number of rows.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    n = output_grid.shape[0]
    
    # Iterate through rows up to the midpoint
    for i in range(n // 2):
        # Swap row i with row n-1-i
        temp_row = np.copy(output_grid[i])
        output_grid[i] = output_grid[n - 1 - i]
        output_grid[n - 1 - i] = temp_row

    return output_grid