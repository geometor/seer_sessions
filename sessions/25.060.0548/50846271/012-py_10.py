"""
Iterate through each pixel in the input grid. If a pixel is red (color value 2), examine its four immediate neighbors: above, below, left, and right. If all four neighboring pixels exist (are within bounds) and have the same color, change the red pixel's color to azure (color value 8). Otherwise, the pixel remains unchanged.
"""

import numpy as np

def get_neighbor_colors(grid, row, col):
    """
    Gets the colors of the four immediate neighbors of a pixel, handling boundary conditions.
    Returns a list of neighbor colors. If a neighbor is out of bounds, its color is not included.
    """
    rows, cols = grid.shape
    neighbor_colors = []

    if row > 0:
        neighbor_colors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbor_colors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbor_colors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbor_colors.append(grid[row, col + 1])  # Right

    return neighbor_colors

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is red
            if input_grid[row, col] == 2:
                # Get neighbor colors
                neighbor_colors = get_neighbor_colors(input_grid, row, col)

                # Check if all neighbors exist (count is 4) and have the same color
                if len(neighbor_colors) == 4 and all(color == neighbor_colors[0] for color in neighbor_colors):
                    # Change the red pixel to azure
                    output_grid[row, col] = 8

    return output_grid