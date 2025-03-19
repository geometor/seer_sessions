"""
The transformation rule involves expanding blue lines from existing blue and green pixels.
Blue pixels expand both horizontally and vertically. Green pixels only expand blue vertically.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of valid (within bounds) neighbors' coordinates (row, col) 
    for a given cell in the grid.  Includes only horizontal and vertical 
    neighbors, not diagonal.
    """
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
    rows, cols = output_grid.shape

    # 1. Identify Seeds: Find all blue (1) and green (3) pixels.
    blue_seeds = np.argwhere(output_grid == 1)
    green_seeds = np.argwhere(output_grid == 3)

    # 2 & 3. Horizontal and Vertical Expansion for Blue Seeds
    for row, col in blue_seeds:
        neighbors = get_neighbors(output_grid, row, col)
        for n_row, n_col in neighbors:
            if output_grid[n_row, n_col] == 0:
                output_grid[n_row, n_col] = 1

    # 3. Vertical Expansion for Green Seeds.
    for row, col in green_seeds:
        neighbors = get_neighbors(output_grid, row, col)

        #filter for only up and down
        for n_row, n_col in neighbors:
          if (n_row == row - 1 and n_col == col) or \
            (n_row == row + 1 and n_col == col):
            if output_grid[n_row, n_col] == 0:
              output_grid[n_row, n_col] = 1

    return output_grid