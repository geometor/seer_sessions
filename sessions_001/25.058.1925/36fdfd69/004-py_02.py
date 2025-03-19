"""
Iterate through each pixel of the input grid. If a pixel is blue (1) and has at
least one red (2) neighbor, change the pixel's color to yellow (4) in the output
grid. Otherwise, keep the pixel's original color.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of neighboring pixel values for a given cell in the grid.
    Neighbors are considered cells sharing a side (up, down, left, right).
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the rule: change blue pixels to yellow if they neighbor red.

    Args:
      input_grid: input array

    Returns: 
        array: output array
    """

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel.
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is blue.
            if input_grid[row, col] == 1:
                # Get the values of the neighboring pixels.
                neighbors = get_neighbors(input_grid, row, col)
                # Check if any neighbor is red.
                if 2 in neighbors:
                    # Change the pixel to yellow in the output grid.
                    output_grid[row, col] = 4

    return output_grid