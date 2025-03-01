"""
Preserves a frame while duplicating select unique interior color pixels.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find single yellow (4) pixel and copy
    yellow_pos = np.where(input_grid == 4)
    if len(yellow_pos[0]) > 0:
      # assuming only on interior
      output_grid[yellow_pos[0][0], yellow_pos[1][0]]

    # Find single Green(3) pixels, and copy, and duplicate it below
    green_pos = np.where(input_grid == 3) # Find single Green(3) pixels
    if len(green_pos[0]) > 0:
      #assuming only on interior
      output_grid[green_pos[0][1], green_pos[1][1]] = 3
      output_grid[green_pos[0][1]+3, green_pos[1][1]] = 3

    # Find single Red(2) pixel, and copy, and duplicate it below
    red_pos = np.where(input_grid == 2)
    if len(red_pos[0]) > 0:
       output_grid[red_pos[0][0], red_pos[1][0]]
       output_grid[red_pos[0][0]+4, red_pos[1][0]]

    return output_grid