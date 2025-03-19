"""
The transformation rule is: white (0) pixels in the input grid shift down by one row, wrapping around from the bottom row to the top. Maroon (9) pixels remain in their original positions. Other color pixels are unaffected by the white pixel movement.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the rule: white pixels shift down one row, wrapping around.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # Apply transformation based on current pixel above
            if r == 0:
                above = input_grid[rows-1,c]
            else:
                above = input_grid[r-1,c]

            if above == 0:
                output_grid[r,c] = 0
            elif input_grid[r, c] == 0:
                output_grid[r,c] = above



    return output_grid