"""
Examine the input 3x3 grid. Identify red pixels ('2').
If red pixels are adjacent (side-by-side or corner diagonal), output is 7.
Otherwise (isolated or only in straight line), output is 1.
"""

import numpy as np

def count_red_pixels(grid):
    """Counts the number of red pixels (value 2) in the grid."""
    return np.sum(grid == 2)

def are_red_pixels_adjacent(grid):
    """Checks if any red pixels are adjacent (horizontally, vertically, or diagonally)."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:
                # Check neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 2:
                            return True
    return False
    
def are_red_pixels_in_line(grid):
    count = 0
    rows, cols =  grid.shape
    #check if all in same row
    for r in range(rows):
      for c in range(cols):
        if grid[r,c] == 2:
          count += 1
      if count > 0 and count < 3:
        if np.sum(grid[r,:]) == 2 * count:
            return True
      count = 0
    count = 0
    #check for all in same col
    for c in range(cols):
      for r in range(rows):
        if grid[r,c] == 2:
          count += 1
      if count > 0 and count < 3:
        if np.sum(grid[:,c]) == 2 * count:
          return True
      count = 0
    
    return False

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation

    #if count_red_pixels(grid) > 0:
    if are_red_pixels_adjacent(grid) and not are_red_pixels_in_line(grid) :
        return 7
    else:
      return 1
