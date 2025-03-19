"""
The input grid is rotated 90 degrees counter-clockwise and  the x and y coordinates are swapped.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Rotate and invert. Iterate through the input grid.
    for x in range(rows):
        for y in range(cols):
            # Apply the transformation: new_x = y, new_y = x.
            new_x = y
            new_y = x
            
            output_grid[new_x, new_y] = input_grid[x,y]
            

    return output_grid.tolist()