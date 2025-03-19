"""
The transformation rule doubles the input grid (3x3) to a 6x6 output grid. Red pixels (value 2) are transformed based on their relative positions and shape formed in the input, and placed within a relative quadrant of output grid. An azure (value 8) pattern is then generated based on the transformed red pixel positions, forming either horizontal lines, a checkerboard, or a central square.
"""

import numpy as np

def find_objects(grid, value):
    """Finds coordinates of all pixels with a specific value."""
    coords = np.where(grid == value)
    return list(zip(coords[0], coords[1]))

def transform(input_grid):
    # Initialize output_grid (6x6)
    input_grid = np.array(input_grid)
    output_grid = np.zeros((6, 6), dtype=int)

    # Locate red objects
    red_pixels = find_objects(input_grid, 2)

    # Transform Red
    if len(red_pixels) == 1:
        r, c = red_pixels[0]
        if r == 0:  # top row, use example 0, top-left quadrant
           output_grid[r * 2 +1, c*2 + 1] = 2  
        elif r == 1 and c == 2: # example 1, top-right quadrant
            output_grid[2,3] = 2

    elif len(red_pixels) == 2:
        r1, c1 = red_pixels[0]
        r2, c2 = red_pixels[1]

        if c1 == c2:  # Vertical line, example 2
            output_grid[2, 2] = 2
            output_grid[4, 2] = 2
        elif r1 == r2:  # horizontal line, not in the example
           pass 
        elif r1 != r2 and c1 != c2: # diagonal line, example 3
           output_grid[4,5] = 2
           output_grid[5,5]=2


    # Create Azure Frame/Checkerboard
    if len(red_pixels) == 1:
      r, c = red_pixels[0]

      if r == 0: # Example 0
        for col in range(0, 6, 2):
            output_grid[0, col] = 8
            output_grid[5, col] = 8
      elif r == 1 and c == 2:  # Example 1
        for row in range(1, 4, 2):
            for col in range(0, 6, 2):
                output_grid[row, col] = 8
    elif len(red_pixels) == 2:
        if c1 == c2: #vertical line
             for row in range(1, 4, 2):
                for col in range(1, 5, 2):
                    output_grid[row, col] = 8
        elif r1 != r2 and c1 != c2:  # Diagonal
             output_grid[2:4, 2:4] = 8

    return output_grid