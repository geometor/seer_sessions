"""
The output grid is created by horizontally flipping each row of the input grid. The dimensions (height and width) of the output grid are identical to the dimensions of the input grid.  Each row in the output is a mirror image (left-to-right reversal) of the corresponding row in the input.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels 
    for i in range(rows):
        output_grid[i] = input_grid[i][::-1]

    return output_grid