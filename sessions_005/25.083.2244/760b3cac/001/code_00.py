"""
The yellow (4) pixels maintain their exact positions in the output grid. 
The azure (8) pixels is moved to the left or to the right, depend on their position and neighbors.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Get the valid neighbors of a cell in a grid."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r, c = row + dr, col + dc
            if 0 <= r < rows and 0 <= c < cols:
                neighbors.append((r, c))
    return neighbors

def count_neighbors_of_same_color(grid, row, col):
    count = 0
    neighbors = get_neighbors(grid,row,col)
    for nr, nc in neighbors:
      if grid[nr,nc] == grid[row,col]:
        count = count + 1
    return count

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Yellow pixels remain unchanged
            if input_grid[r, c] == 4:
                continue  # Yellow pixels are already in place

            # Handle azure pixels
            if input_grid[r, c] == 8:
                neighbors_count = count_neighbors_of_same_color(input_grid,r,c)
                if neighbors_count < 2:
                  #move isolated to left, if it is possible
                  if input_grid[r,0] == 0:
                    output_grid[r,c] = 0
                    output_grid[r,0] = 8
                  else:
                    #otherwise, move it to right
                    output_grid[r,c] = 0
                    output_grid[r,cols-1] = 8
                else:
                  #mirror connected
                  output_grid[r,c] = 0
                  output_grid[r,cols-1-c] = 8

    return output_grid