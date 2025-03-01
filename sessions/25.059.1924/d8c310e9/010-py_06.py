"""
1.  **Copy the last row:** Copy the last row of the input grid directly to the last row of the output grid.
2.  **Copy red blocks:** Copy the vertical red blocks (color 2) in rows 3 and 4, columns 2 and 6 in the input grid to the same location in the output grid.
3.  **Extend:** For any red block detected in the third and fourth rows, mirror those red blocks two cells to their right.
4. **Fill empty cells** Every other cell will remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Copy the last row (already done during initialization)

    # Iterate through the grid to find and extend red blocks
    for r in range(rows -1):
        for c in range(cols):
            if input_grid[r][c] == 2:
                # Copy existing red blocks (already in place due to copy)

                # Extend red blocks to the right
                if c + 2 < cols :
                    output_grid[r, c + 2*4] = 2
                    if input_grid[r+1,c] == 2: # make sure to copy it if and only if it is two long.
                        output_grid[r+1,c+2*4] = 2


    return output_grid