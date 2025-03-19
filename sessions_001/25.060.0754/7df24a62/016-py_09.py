"""
1.  **Identify** all yellow (4) and blue (1) pixels in the input grid.
2.  **Iterate** through yellow pixels.
3.  **Check** the 3x3 neighborhood centered on each yellow pixel.
    *   If a blue pixel from the originally identified is in the neighborhood, change to blue.
4.  **Iterate** through input.
5.  **Check** 3x3 neighborhoods.
    *   if original neighborhood contains both 1 and 4, the centered pixel change to 1.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 3x3 neighborhood around a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify yellow and blue pixels
    yellow_pixels = []
    blue_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 4:
                yellow_pixels.append((r, c))
            elif input_grid[r, c] == 1:
                blue_pixels.append((r, c))

    # 2. Iterate through yellow pixels and check neighborhood
    for r, c in yellow_pixels:
        neighbors = get_neighbors(input_grid, r, c)
        if 1 in neighbors:
              output_grid[r,c] = 1

    # 3. Iterate all output pixels and fill
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(input_grid, r, c)
            if (1 in neighbors) and (4 in neighbors):
                output_grid[r,c] = 1

    return output_grid