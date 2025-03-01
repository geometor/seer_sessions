"""
The transformation rule is as follows:
1. Observe the input grid's dimensions.
2. Create a new grid with the same dimensions.
3. Iterate through each cell of the input grid.
4. If a cell has value 0, fill it in the output with alternating values of 8 and 1, starting with 8.
5. If the input cell value is 1, it also get the alternating 8, 1 sequence, but where the position fits into the pattern that was started at 0,0 determines where it starts.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:
                if (i + j) % 2 == 0:
                    output_grid[i, j] = 8
                else:
                    output_grid[i, j] = 1
            else: # input_grid[i,j] == 1
                if (i + j) % 2 == 0:
                    output_grid[i,j] = 1
                else:
                    output_grid[i,j] = 8

    return output_grid