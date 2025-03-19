"""
The transformation rule takes a 1xN input grid and generates an output grid where the red (2) pixels from the input are expanded into a square in the top-left corner, while the white (0) pixels remain white. The size of the red square grows based on the number of red pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same width as the input and determined height.
    rows = 0
    for x in range(len(input_grid[0])):
      if input_grid[0][x] == 2:
        rows +=1
    output_grid = np.zeros((rows, len(input_grid[0])), dtype=int)

    # Find the red pixels in the input grid.
    
    # Create the square of red pixels.
    for i in range(rows):
        for j in range(min(i + 1,len(input_grid[0]))):
            output_grid[i, j] = 2

    # Fill the remaining cells with white (0).
    #output_grid[output_grid == 0] = 0  # This line is redundant as the grid is initialized with 0s.
    
    return output_grid