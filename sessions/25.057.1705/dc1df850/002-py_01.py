"""
The transformation rule is as follows:
1. Identify all red (2) pixels in the input grid.
2. Propagate red: For each red pixel, change adjacent white pixels to blue.
3. Preserve other colors: Maintain the color and position of all other non-white pixels (e.g., the magenta pixel).
"""

import numpy as np

def get_red_pixels(grid):
    # Find coordinates of all red pixels.
    red_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r,c] == 2:
                red_pixels.append((r,c))
    return red_pixels
    
def get_adjacent_white_pixels(grid, r, c):
  #find all white cells next to the input cell (r,c)
  adjacent_white = []
  for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
      if dr == 0 and dc == 0:
        continue
      
      nr, nc = r + dr, c + dc
      if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] == 0:
        adjacent_white.append((nr, nc))
  return adjacent_white
  
def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)

    # Get coordinates of red pixels.
    red_pixels = get_red_pixels(input_grid)

    # Iterate over red pixels.
    for r, c in red_pixels:
        #output_grid[r, c] = 2 # keep red pixels as they were
        adjacent_whites = get_adjacent_white_pixels(input_grid,r,c)
        for ar, ac in adjacent_whites:
            output_grid[ar,ac] = 1
        
    return output_grid