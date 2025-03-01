"""
The azure shape has its left-side pixels recolored to red. The core concept here the idea of 'left side' - the azure pixels change color to red by 'filling in' any indentations on the shape.
"""

import numpy as np

def find_azure_shape(grid):
    # Find the coordinates of all azure (8) pixels.
    azure_coords = np.argwhere(grid == 8)
    return azure_coords

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the azure shape.
    azure_coords = find_azure_shape(output_grid)
    if len(azure_coords) == 0:
        return output_grid

    # Find the leftmost azure pixels.
    min_col = np.min(azure_coords[:, 1])

   # Iterate through all azure pixels
    for r, c in azure_coords:
      # check if the pixel to the left is white
      if c>0 and output_grid[r,c-1] == 0:
          # start recoloring path
          temp_c = c
          while temp_c >= min_col and output_grid[r, temp_c] == 8:
            output_grid[r,temp_c] = 2
            temp_c -= 1
            

    return output_grid