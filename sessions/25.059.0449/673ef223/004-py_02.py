"""
Transforms the input grid by expanding an azure region horizontally, introducing a yellow pixel, and maintaining red lines.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of all pixels of the specified color.
    objects = []
    rows, cols = np.where(grid == color)
    for r, c in zip(rows, cols):
        objects.append((r, c))
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find the red and azure pixels.
    red_pixels = find_objects(input_grid, 2)
    azure_pixels = find_objects(input_grid, 8)

    # Left red line and azure transformation.
    for r, c in azure_pixels:
      if c < input_grid.shape[1] / 2: #check for left side
        for i in range(3):
            if c - i -1 >= 0: # check boundary, don't go past edge
                output_grid[r, c - i - 1] = 8  # Expand azure to the left.
        if c+1 < input_grid.shape[1]:  #check boundary condition
             output_grid[r, c + 1] = 4      # Add a yellow pixel to the right.

    #Right red line transformation
    for r, c in red_pixels:
        if c > input_grid.shape[1] /2: #check for right hand side
            for i in range(6):
                if c - i - 1 >=0: #check boundary, don't go past edge
                    output_grid[r,c-i-1] = 8



    return output_grid