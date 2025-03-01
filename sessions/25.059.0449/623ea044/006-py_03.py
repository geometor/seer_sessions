"""
Transforms an input grid by identifying the location of the red pixel (value 2) and drawing two lines of red pixels. One horizontal line extends to the right, and the other vertical line extends downwards, both from the position of the original red pixel.
"""

import numpy as np

def find_origin(grid):
    # Find the coordinates of the single red pixel (value 2)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 2:
                return (i, j)
    return None

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.array(input_grid, copy=True)  # Start with a copy, modify copy
    origin = find_origin(input_grid)

    if origin is None:
        return output_grid  # Return unchanged if no red pixel is found

    row, col = origin
    height, width = input_grid.shape

    # Draw vertical line downwards
    for i in range(row, height):
      output_grid[i,col] = 2
    
    # Draw Horizontal line to the right
    for j in range(col, width):
      output_grid[row,j] = 2
    
    return output_grid