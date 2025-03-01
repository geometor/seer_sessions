"""
Identify existing colored pixels (non-white pixels) in the input grid.

For each colored pixel:

- If the colored pixel is blue (1), place orange (7) pixels adjacent to it, both horizontally and vertically, if empty.
- If the colored pixel is red (2), place a yellow(4) pixels adjacent, both horizontally and vertically, if empty.
- Magenta (6) is not affected, it is copied to same place.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    returns a list if valid neighbor coordinates
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
    """
    Transforms the input grid according to the specified rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            pixel = input_grid[row, col]
            
            # skip white pixel
            if pixel == 0:
                continue

            neighbors = get_neighbors(input_grid, row, col)

            if pixel == 1:  # Blue
                for r, c in neighbors:
                    if output_grid[r,c] == 0: # if white, change it
                        output_grid[r, c] = 7  # Orange
            elif pixel == 2:  # Red
                for r, c in neighbors:
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 4  # Yellow

    return output_grid