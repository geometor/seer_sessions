"""
The transformation rule involves propagating non-zero values from the right and bottom edges of the input grid. The bottom-right corner's value, if non-zero, becomes dominant and fills the bottom-right 2x2 subgrid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify the key color (bottom-right cell)
    key_color = output_grid[rows - 1, cols - 1]

    # Vertical Propagation (from right to left)
    for j in range(cols - 1, -1, -1):
        for i in range(rows - 1, -1, -1):
            if output_grid[i,j] != 0 :
                for k in range(i+1, rows):
                    if(output_grid[k,j] == 0):
                        output_grid[k, j] = output_grid[i,j]
                    else:
                        break

    # bottom row propagation
    for j in range(cols-1):
         if output_grid[rows-1,j] != 0:
            for k in range(j+1,cols):
                if output_grid[rows-1,k] == 0:
                    output_grid[rows-1,k]=output_grid[rows-1,j]
                else:
                    break
    
    #fill the corner
    if key_color != 0:
        output_grid[rows-1, cols-1] = key_color
        if rows >= 2 and cols >= 2:
           output_grid[rows-2, cols-1] = key_color
           output_grid[rows-1, cols-2] = key_color


    return output_grid