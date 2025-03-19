"""
Iterate through each pixel in the input grid.
  If a pixel is blue, determine if it is isolated by searching for other blue pixels in the eight adjacent cells.
      if a pixel is isolated, it should remain blue.
  If a pixel is blue and is connected, it should also remain blue.
  All other pixels should remain the same.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8 neighbors of a cell (including diagonals)."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the cell itself
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:  # If it's a blue pixel
                neighbors = get_neighbors(input_grid, row, col)
                if 1 in neighbors:  # Check for adjacent blue pixels
                    output_grid[row, col] = 1  # remains blue
                else: # isolated blue pixel
                    output_grid[row,col] = 1 # remains blue

    return output_grid