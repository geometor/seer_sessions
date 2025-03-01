"""
The input 2x2 grid is replicated four times to form the 4x4 output grid. The top-left cell of the input becomes the top-left, top-right, bottom-left, and bottom-right 2x2 quadrants of the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)

    # change output pixels 
    for i in range(2):
        for j in range(2):
            output_grid[i*2][j*2] = input_grid[i][j]
            output_grid[i*2+1][j*2] = input_grid[i+1][j]
            output_grid[i*2][j*2+1] = input_grid[i][j+1]
            output_grid[i*2+1][j*2+1] = input_grid[i+1][j+1]

    return output_grid