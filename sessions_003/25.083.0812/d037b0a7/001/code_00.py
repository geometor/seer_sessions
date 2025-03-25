"""
1.  **Identify Seed Pixels:** Find all non-zero (non-black) pixels along the top edge (row 0) and left edge (column 0) of the input grid.

2.  **Column Propagation:** For each non-zero pixel found on the top edge, iterate through the cells in its column. Change the color of each cell in that column to match the color of the seed pixel on the top edge.

3.  **Row Propagation:** For each non-zero pixel found on the left edge, iterate through the cells in its row, from left to right. Change the color of each cell in that row to match the color of the seed pixel at the left edge.

4.  Propagation order matters, first do columns, then do rows.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    height = len(input_grid)
    width = len(input_grid[0])

    # Column Propagation
    for j in range(width):
        if input_grid[0][j] != 0:
            for i in range(height):
                output_grid[i][j] = input_grid[0][j]

    # Row Propagation
    for i in range(height):
        if input_grid[i][0] != 0:
            for j in range(width):
                output_grid[i][j] = input_grid[i][0]

    return output_grid