"""
The top row of the grid is modified. The white pixels (0) in the top row are replaced with the color in the cell that is in the same column and the cell is not in the top row, and is furthest from the top row. If the pixel is not white then, there is no change to the top row.. Other rows are are not changed.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0])

    # change output pixels 
    for j in range(cols):
        if input_grid[0][j] == 0:
           output_grid[0][j] = input_grid[rows-1][j]

    return output_grid