"""
Identifies the positions of blue (1) and red (2) pixels in the input grid.
Preserves these positions in the output grid.
Fills columns to the right of the blue pixel, alternating every other column with blue (1), until x=4 inclusive.
Fills columns to the right of the red pixel, alternating every other column with red (2), until x=9 inclusive.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first occurrence of a specified color."""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = np.zeros((rows, cols), dtype=int)

    # Find blue and red pixels
    blue_pos = find_pixel(input_grid, 1)
    red_pos = find_pixel(input_grid, 2)

    # Preserve original pixel positions, if found
    if blue_pos:
        output_grid[blue_pos] = 1
    if red_pos:
        output_grid[red_pos] = 2
        
    # Columnar fill - Blue, until column index 4
    if blue_pos:
      for x in range(blue_pos[1] + 1, 5):
          if (x - blue_pos[1]) % 2 != 0: # Check for odd columns relative to blue_pos
              for y in range(rows):
                  output_grid[y,x] = 1

    # Columnar fill - Red, until column index 9
    if red_pos:      
      for x in range(red_pos[1] + 1, min(10, cols)):  # Stop at column 9 or end of grid
          if (x - red_pos[1]) % 2 != 0:  # Check for odd columns relative to red_pos
              for y in range(rows):
                  output_grid[y,x] = 2

    return output_grid