"""
1.  **Copy** the first row of the input grid directly to the first row of the output grid.
2.  **Copy** all rows of the input grid that are comprised of all the same color (all 7s, orange in this case), besides the first 2 rows, directly to the output.
3.  **Transform Row 2**: inspect input grid row 2, and do the following:
    *   starting at the third element, and for the remainder of row 2.
    *   inspect the element above (from row 1).
    *   if row 1's color to the right is different, copy the different color value from row 1's element on the right to row 2.
    *   else (if the color is the same or does not exist) set the color to the previous value from row 2.
4. copy all other rows, if any, to the output, unchanged.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Transform Row 2
    for j in range(1, cols):
        if j + 1 < cols:  # Ensure we don't go out of bounds
            if input_grid[0, j] != input_grid[0, j + 1]:
                output_grid[1, j] = input_grid[0, j+1]
            else:
                output_grid[1,j] = output_grid[1,j-1]
        elif j>0:
            output_grid[1,j] = output_grid[1, j-1]

    return output_grid.tolist()