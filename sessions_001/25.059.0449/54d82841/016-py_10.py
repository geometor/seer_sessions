"""
The input is a 5x7 grid. The first four rows of the input grid are copied to the output grid. 
In the last row (index 4), replace some white (0) pixels with yellow (4) pixels. 
The white pixels to be replaced are those that align with the columns containing azure (8) or magenta (6) blocks in row index 2.
"""

import numpy as np

def get_neighbors(grid, r, c):
    rows, cols = grid.shape
    neighbors = []
    if c > 0:
      neighbors.append(grid[r, c-1])
    if c < cols-1:
      neighbors.append(grid[r,c+1])
    return neighbors

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Iterate through the input grid.
    #Copy the first four rows
    
    # Modify the last row (index 4) based on row 2.
    for c in range(cols):
      if input_grid[rows-1,c] == 0:
          if input_grid[2,c] != 0:
              output_grid[rows - 1, c] = 4

    return output_grid