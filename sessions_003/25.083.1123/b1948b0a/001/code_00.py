"""
Iterate through each pixel of the input grid. If a pixel has the color 6 (magenta) and has a neighbor of color 7 (orange), change its color to 2 (red). Otherwise, keep the original color.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Get the neighbors of a pixel, only adjacent.
    """
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append(grid[row-1, col])
    if row < rows - 1:
        neighbors.append(grid[row+1, col])
    if col > 0:
        neighbors.append(grid[row, col-1])
    if col < cols - 1:
        neighbors.append(grid[row, col+1])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    # Initialize the output grid with the same dimensions and data type as the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate over each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is magenta (6)
            if input_grid[row, col] == 6:
                # Get the neighbors of the current pixel
                neighbors = get_neighbors(input_grid, row, col)
                # Check if any of the neighbors are orange (7)
                if 7 in neighbors:
                    # Change the corresponding pixel in the output grid to red (2)
                    output_grid[row, col] = 2

    # Return the modified grid
    return output_grid