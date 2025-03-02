"""
Identify blue (1) pixels in the input grid. Iterate through each pixel in the grid. If a pixel is adjacent to a blue pixel, change its color to azure (8).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns the neighbors of a pixel, the 8 pixels surrounding it
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    # Initialize the output grid with the same values as the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is blue. if is, continue.
            if input_grid[row, col] == 1:
                continue

            # Get the neighbors of current pixel
            neighbors = get_neighbors(input_grid, row, col)

            # Check neighbors' color, change pixel color to azure if a neighbor is blue.
            if 1 in neighbors:
                output_grid[row, col] = 8

    return output_grid