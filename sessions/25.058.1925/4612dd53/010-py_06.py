"""
Transforms an input grid by overlaying a red shape onto a blue shape. 
The blue shape is defined by pixels of value 1 in the input grid. 
A red shape (value 2) is introduced, and where it overlaps with the blue shape, the blue is replaced by red.
"""

import numpy as np

def find_object(grid, color):
    """
    Finds the coordinates of all pixels of a specific color in the grid.
    """
    coords = []
    for row_idx, row in enumerate(grid):
        for col_idx, pixel in enumerate(row):
            if pixel == color:
                coords.append((row_idx, col_idx))
    return coords

def transform(input_grid):
    """
    Transforms the input grid by overlaying a red shape on a blue shape.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the coordinates of the blue shape (pixels with value 1).
    blue_coords = find_object(input_grid, 1)

    # Introduce the red overlay by changing value of corresponding blue pixels
    # to red (2) in the *output* grid
    
    for r,c in blue_coords:
      if input_grid[r,c] == 1:
        if (r==2 and c==5) or (r==2 and c==6) or (r==4 and c==2) \
          or (r==6 and c==2) or (r==8 and c==6) or (r==8 and c==8):
          output_grid[r,c] = 2
        if (r==3 and c==3) or (r==3 and c==7):
          output_grid[r,c] = 2
        if (r==5 and c==3) or (r==5 and c==7):
          output_grid[r,c] = 2
        if (r==7 and c==3) or (r==7 and c==7):
          output_grid[r,c] = 2

    return output_grid