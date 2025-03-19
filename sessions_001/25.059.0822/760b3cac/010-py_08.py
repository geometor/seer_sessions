"""
The transformation rule is as follows:

1.  **Identify Objects:** Locate the contiguous blocks of azure (8) and yellow (4) pixels.
2.  **Focus on Azure Shape:** Analyze the azure shape.
3.  **Expansion Rule:**, find all the '0' on the first row that are adjacent to '8', change it to '8'. Find the '8' on the first row. For each '8' on the first row, change the '0' below it to '8'.
4.  **Yellow shape** remains unchanged.
"""

import numpy as np

def get_adjacent(grid, r, c, color):
    rows, cols = len(grid), len(grid[0])
    adjacent_pixels = []

    # Check adjacent cells (up, down, left, right)
    if r > 0 and grid[r-1][c] == color:
        adjacent_pixels.append((r-1, c))  # Up
    if r < rows - 1 and grid[r+1][c] == color:
        adjacent_pixels.append((r+1, c))  # Down
    if c > 0 and grid[r][c-1] == color:
        adjacent_pixels.append((r, c-1))  # Left
    if c < cols - 1 and grid[r][c+1] == color:
        adjacent_pixels.append((r, c+1))  # Right

    return adjacent_pixels
def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = len(output_grid), len(output_grid[0])

    # fill right
    for c in range(cols - 1):
        if output_grid[0][c] == 8 and output_grid[0][c+1] == 0:
             output_grid[0][c+1] = 8

    #fill down
    for r in range(rows - 1):
        for c in range(cols):
            if output_grid[r][c] == 8:
                if output_grid[r+1][c] == 0 :
                    output_grid[r+1][c] = 8

    return output_grid