"""
The input grid is doubled in both dimensions. 
A new color (azure) is introduced. 
The output grid follows a pattern: original pixel, white pixel, azure pixel, original pixel, white pixel, azure pixel.
Original input pixels are mapped to their corresponding positions in the expanded grid.
Remaining positions are filled with azure, maintaining the specified pattern.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2, input_cols * 2
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # change output pixels according to the described pattern
    for i in range(input_rows):
        for j in range(input_cols):
            output_grid[i * 2, j * 3] = input_grid[i, j]
            output_grid[i*2, (j*3) + 2] = 8
            
            output_grid[(i * 2)+1, (j*3) +2] = 8
            output_grid[(i*2) + 1, j*3] = input_grid[i,j] if input_grid[i,j] != 0 else 8

    return output_grid