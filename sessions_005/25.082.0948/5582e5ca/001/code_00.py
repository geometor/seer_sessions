"""
The input 3x3 grid is transformed into a 3x3 output grid where all cells have the same value.
The value to fill output grid is taken from center element of the input grid.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the center value of input_grid
    center_value = input_grid[1][1]

    # Fill every cell of the output grid with the center value
    for i in range(3):
        for j in range(3):
            output_grid[i][j] = center_value
    
    return output_grid