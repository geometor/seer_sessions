"""
Embed the 3x3 input grid into the top-left corner of a 6x6 output grid. 
Reflect the input grid horizontally into the top-right quadrant. 
Then, reflect the entire top half of the output grid vertically to fill the bottom half.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a 6x6 array filled with zeros.
    output_grid = np.zeros((6, 6), dtype=int)

    # Embed the input_grid into the top-left corner of the output_grid.
    output_grid[:3, :3] = input_grid
    
    # Reflect horizontally into top-right
    rows, cols = input_grid.shape
    for i in range(rows):
        for j in range(cols):
            output_grid[i, 3 + (cols - 1 - j)] = input_grid[i, j]

    # Reflect the entire top half vertically.
    for i in range(3):
        for j in range(6):
            output_grid[5-i,j] = output_grid[i,j]

    return output_grid