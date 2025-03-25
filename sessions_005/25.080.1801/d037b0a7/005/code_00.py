"""
1.  **Identify "filled" cells:** A cell in the original input grid is considered "filled" if it has a non-zero value.
2.  Iterate every row.
3.  If cell was "filled" propogate the value down and right.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Iterate through each cell of the input_grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell was "filled" (non-zero)
            if input_grid[r, c] != 0:
                # Propagate the value downwards and to the right
                for r_down in range(r + 1, rows):
                    output_grid[r_down, c] = output_grid[r, c]
                for c_right in range(c+1, cols):
                    output_grid[r, c_right] = output_grid[r, c]
                for r_down in range(r+1, rows):
                  for c_right in range(c+1, cols):
                    output_grid[r_down, c_right] = output_grid[r,c]
    return output_grid