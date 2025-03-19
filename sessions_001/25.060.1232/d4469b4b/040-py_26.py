"""
The transformation involves reducing a 5x5 grid to a 3x3 grid, and recoloring the green areas of the original as gray areas in the output.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as 3x3, filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Create a mapping for 3x3 sections to new coordinates
    mapping = {
        (0, 0): (0, 2),
        (0, 1): (0, 2),
        (1, 0): (0, 2),
        (1, 1): (0, 2),
        (0, 3): (0, 2),
        (0, 4): (0, 2),
        (1, 3): (0, 2),
        (1, 4): (0, 2),
      
        (3, 0): (2, 0),
        (3, 1): (2, 0),
        (3, 2): (2, 2),
        (4, 0): (2, 0),
        (4, 1): (2, 0),
        (4, 2): (2, 2),
    }

    # Iterate through the input grid and map values to the output grid
    for i in range(input_grid.shape[0]):
       for j in range(input_grid.shape[1]):
           if input_grid[i,j] == 3:
              if (i,j) in mapping:
                x,y = mapping[(i,j)]
                output_grid[x,y] = 5
    return output_grid