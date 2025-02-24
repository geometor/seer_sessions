"""
1.  **Identify Red Pixels:** Locate all pixels with the value 2 (red).
2.  **Identify Adjacent Blue Pixels:** For each red pixel, or group of contiguous red pixels, find all adjacent blue pixels (value 1). Adjacency includes directly above, below, left, and right.
3.  **Change to White:** Change all of these identified adjacent blue pixels to white (value 0).
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the coordinates of adjacent pixels (up, down, left, right).
    """
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent.append((row + 1, col))  # Down
    if col > 0:
        adjacent.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent.append((row, col + 1))  # Right
    return adjacent

def transform(input_grid):
    # initialize output_grid as a copy of input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # identify red pixels
    red_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2:
                red_pixels.append((r, c))

    # find blue pixels adjacent to red pixels
    blue_to_white = set()
    for r, c in red_pixels:
        adjacent = get_adjacent_pixels(input_grid, r, c)
        for ar, ac in adjacent:
            if input_grid[ar, ac] == 1:
                blue_to_white.add((ar, ac))
    
    # change blue to white
    for r, c in blue_to_white:
      output_grid[r,c] = 0
      

    return output_grid