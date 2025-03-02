"""
The transformation rule is as follows:
1. Iterate through all pixels.
2. If a pixel is green determine if there is a white neighbor. If so, leave it green. If a pixel is completely surrounded by green, change it to yellow.
3. If there is no background, do not make any transformations.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col - 1])  # Right
    return neighbors

def has_white_neighbor(grid, row, col):
    """Checks if a cell has any white neighbors."""
    neighbors = get_neighbors(grid, row, col)
    return any(neighbor == 0 for neighbor in neighbors)

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Check if the grid has a white background (any white pixels)
    if 0 not in input_grid:
      return output_grid

    # Iterate through each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is green (3)
            if input_grid[row, col] == 3:
                neighbors = get_neighbors(input_grid, row, col)
                # Check if all neighbors are also green (3)
                if all(neighbor == 3 for neighbor in neighbors):
                    output_grid[row, col] = 4  # Change to yellow (4)

    return output_grid