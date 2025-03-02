"""
The transformation rule can be summarized as follows:

1.  **Copy the Grid:** Start with a copy of the input grid.
2.  **Preserve White:** All white (0) pixels in the input remain white (0) in the output.
3.  **Preserve Green regions**: Maintain green (3) in output, except adjacent to red.
4.  **Modify Red:**
    *   If a red pixel is next to existing green, it and all adjacent pixels become red in output.
    *   If a single red pixel exists in the input, the three pixels above are converted to `3 2 3` respectively.
    *   If there are adjacent reds in a line, replace those with a solid red line.
"""

import numpy as np

def get_neighbors(grid, r, c, include_diagonal=False):
    """Gets the neighbors of a cell, optionally including diagonals."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0) or (not include_diagonal and (abs(i) + abs(j) != 1)):
                continue
            nr, nc = r + i, c + j
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Preserve white pixels
    # (already handled by copying the grid)

    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                red_pixels.append((r, c))

    # Modify red and adjacent pixels
    for r, c in red_pixels:
      neighbors = get_neighbors(input_grid,r,c)
      is_single = True
      for nr, nc in neighbors:
          if input_grid[nr,nc] == 2:
            is_single = False
            break      
      if is_single:
            if r > 2:
              output_grid[r - 3, c] = 3
              output_grid[r - 2, c] = 2
              output_grid[r - 1, c] = 3

    
    red_pixels = [] # refresh after first pass, can change
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                red_pixels.append((r, c))
    
    for r, c in red_pixels:
      neighbors = get_neighbors(input_grid,r,c)
      for nr, nc in neighbors:
          if output_grid[nr,nc] == 3:
            output_grid[nr,nc] = 2 # make all neighbors of reds = red



    return output_grid