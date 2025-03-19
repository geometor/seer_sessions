"""
The input grid is transformed into an output grid of the same dimensions where all pixels are either gray or white. The determination of which rows are gray depends on the height of the input grid. If the height is odd, the middle row (calculated as integer division of height by 2) is set to gray. If the height is even, the two middle rows (calculated as height // 2 -1 and height // 2) are gray. All other rows are white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    height = input_grid.shape[0]

    # Calculate the middle row index(es)
    middle_row_index = height // 2

    # change output pixels 
    if height % 2 == 1:
        # Odd height: middle row is gray
        output_grid[middle_row_index, :] = 5
    else:
        # Even height: two middle rows are gray
        output_grid[middle_row_index - 1, :] = 5
        output_grid[middle_row_index, :] = 5

    return output_grid