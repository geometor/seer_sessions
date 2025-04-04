"""
1.  **Identify** all yellow (4) and blue (1) pixels in the input grid.
2.  **Iterate** through yellow pixels.
3.  **Check** the 3x3 neighborhood centered on each yellow pixel.
    *   If a blue pixel is in the neighborhood, change *all* yellow pixels in the neighborhood to blue.
4.  **Iterate** through all pixels in grid.
5. **Check** 3x3 neighborhood.
    *    If the input neighborhood contains both blue and yellow and the center pixel is not red, change the center pixel to blue.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 3x3 neighborhood around a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            neighbors.append((i, j, grid[i, j]))  # Store coordinates with the value
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
        if any(pixel[2] == 1 for pixel in neighbors):  # Check if any neighbor is blue
            # Change *all* yellow pixels in the neighborhood to blue
            for nr, nc, color in neighbors:
                if color == 4:
                    output_grid[nr, nc] = 1

    # 3. Iterate through *all* pixels and their neighborhoods
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(input_grid, r, c)
            neighbor_colors = [pixel[2] for pixel in neighbors]
            if 1 in neighbor_colors and 4 in neighbor_colors and input_grid[r,c] != 2:
                output_grid[r, c] = 1


    return output_grid