"""
Iterate through each pixel of the input grid. If a pixel is blue (color value 1), count its immediate blue neighbors (up, down, left, right).
If the number of blue neighbors is exactly two, change the pixel's color to red (color value 2). Otherwise, leave the pixel unchanged.
Pixels that are not blue are not changed.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the values of the four immediate neighbors (up, down, left, right) of a given pixel.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row-1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row+1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col-1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col+1])  # Right
    return neighbors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each pixel in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is blue (1)
            if input_grid[row, col] == 1:
                # Get the values of the four immediate neighbors
                neighbors = get_neighbors(input_grid, row, col)
                # Count how many neighbors are blue (1)
                blue_neighbors_count = neighbors.count(1)
                # If exactly two neighbors are blue, change the pixel to red (2)
                if blue_neighbors_count == 2:
                    output_grid[row, col] = 2

    return output_grid