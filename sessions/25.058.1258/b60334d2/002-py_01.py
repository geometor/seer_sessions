"""
The transformation preserves the gray (value 5) "objects" and generates a checkerboard pattern of 1's and 0's *around* and emanating from them, originating from those object locations. New patterns don't override each other.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Objects (gray pixels)
    object_locations = np.argwhere(input_grid == 5)

    # 2. Create Checkerboard Pattern around each object
    
    processed = set()
    
    for r, c in object_locations:
        output_grid[r,c] = 5
        queue = [(r,c)]
        
        while queue:
          curr_r, curr_c = queue.pop(0)
          
          if (curr_r, curr_c) in processed:
            continue;
            
          processed.add((curr_r,curr_c))
          
          neighbors = get_neighbors(input_grid, curr_r, curr_c)
          
          if output_grid[curr_r, curr_c] == 5 or output_grid[curr_r,curr_c] == 0:
              for nr, nc in neighbors:
                  if input_grid[nr,nc] == 0 and output_grid[nr,nc] == 0 :
                      output_grid[nr, nc] = 1
                      queue.append((nr,nc))
          elif output_grid[curr_r, curr_c] == 1:
            for nr, nc in neighbors:
                if input_grid[nr,nc] == 0 and output_grid[nr,nc] == 0:
                    output_grid[nr, nc] = 0
                    queue.append((nr,nc))


    return output_grid