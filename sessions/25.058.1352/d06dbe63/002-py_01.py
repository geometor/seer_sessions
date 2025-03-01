"""
The transformation rule involves identifying an azure pixel (value 8) in the input grid and generating an "L"-shaped path of gray pixels (value 5) originating from the azure pixel's location. The "L" shape can have variable length/orientation.
"""

import numpy as np

def find_azure_pixel(grid):
    # Find the coordinates of the azure pixel (value 8).
    for r, row in enumerate(grid):
        for c, value in enumerate(row):
            if value == 8:
                return (r, c)
    return None  # Should not happen, based on task description, but good practice.

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    
    # Find the azure pixel.
    azure_pos = find_azure_pixel(input_grid)

    if azure_pos is None:
        return output_grid # Should not happen, input always contains azure pixel
    
    r, c = azure_pos

    # Hardcode an L shape for now, starting in the up-left direction.
    # We'll refine this in later iterations to handle different orientations
    # and potentially a more general path-finding approach.
    
    if r > 2 and c > 2:
      output_grid[r-1, c] = 5
      output_grid[r-2, c] = 5
      output_grid[r-3, c] = 5
      output_grid[r-3, c-1] = 5
      output_grid[r-3, c-2] = 5
    elif r < 10 and c > 2 :
      output_grid[r+1, c] = 5
      output_grid[r+2, c] = 5
      output_grid[r+3, c] = 5
      output_grid[r+3, c-1] = 5
      output_grid[r+3, c-2] = 5
    elif r < 10 and c < 10 :
      output_grid[r+1, c] = 5
      output_grid[r+2, c] = 5
      output_grid[r+3, c] = 5
      output_grid[r+3, c+1] = 5
      output_grid[r+3, c+2] = 5
    elif r > 2 and c < 10 :
      output_grid[r-1, c] = 5
      output_grid[r-2, c] = 5
      output_grid[r-3, c] = 5
      output_grid[r-3, c+1] = 5
      output_grid[r-3, c+2] = 5


    return output_grid