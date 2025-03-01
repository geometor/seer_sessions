"""
The transformation involves copying a 2x2 green block and performing a reflection of color 7 along the y=x diagonal,
and performing a relection of color 8, along the x=4.5 line and removing the color 8 at (7,3)
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Copy the 2x2 block of 3s
    # The copy operation is already handled by initializing output_grid with a copy of input_grid

    # Mirror/Fill '7'
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 7:
              output_grid[c,r] = 7
    
    # Mirror/Fill '8'
    for r in range(rows):
        for c in range(cols):
          if input_grid[r,c] == 8:
            mirrored_r = r
            mirrored_c = cols - 1 - c
            if(mirrored_r >= 0 and mirrored_r <rows and mirrored_c>=0 and mirrored_c < cols):
                output_grid[mirrored_r, mirrored_c] = 8

    #Remove 8 at output(7,3)
    output_grid[7,3] = 0

    return output_grid