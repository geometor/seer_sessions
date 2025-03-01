"""
The transformation rule involves identifying the initial positions of colored pixels (azure, blue, and red) and then extending a pattern vertically. 
The pattern is created by placing blue pixels in every other column, starting from the second column, and then azure pixels in every other empty spot in the second and last rows. 
The remaining areas are filled with a combination of the input pixels and the extended blue pattern.
"""

import numpy as np

def get_colored_pixels(grid, colors):
    """
    Finds the coordinates of pixels of specified colors.
    """
    coords = []
    for color in colors:
        coords.extend(list(zip(*np.where(grid == color))))
    return coords

def transform(input_grid):
    """
    Transforms the input grid according to the identified rules.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Initial State: Get initial colored pixel coordinates
    colored_pixels = get_colored_pixels(input_grid, [1, 2, 8])

    # 2. Create Blue Columns: Vertical extension and filling for blue
    for r in range(rows):
      for c in range(1, cols - 1):  # Start from the second column, end before the last
          if (c % 2) != 0:
            output_grid[r, c] = 1

    # 4. Preserve Initial colored pixels
    for r, c in colored_pixels:
        output_grid[r, c] = input_grid[r, c]
    
    # 3. Place Azure Pixels: Fill azure
    for c in range(1, cols - 1): # Start from the second column, end before the last
      if output_grid[1, c] == 0:  # Check if the spot is empty
        if (c % 2) == 0:
          output_grid[1, c] = 8
      if output_grid[rows - 2, c] == 0:  # Check if the spot is empty
        if (c % 2) == 0:
          output_grid[rows - 2, c] = 8

    return output_grid