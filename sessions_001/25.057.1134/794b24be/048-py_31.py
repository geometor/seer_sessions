"""
1. Iterate through each pixel of the input grid.
2. Check the current pixel's color.
3. If the current pixel is blue (1) and any of its immediate horizontal or vertical neighbors is also blue (1), then change the current pixel's color to red (2) in the output grid.
4. Otherwise, copy input grid pixel to output grid
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Get the immediate horizontal and vertical neighbors of a pixel."""
    neighbors = []
    rows, cols = grid.shape
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
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input_grid
    for row in range(rows):
        for col in range(cols):
            # Get the current pixel's color
            current_color = input_grid[row, col]
            # Get the neighboring pixels' colors
            neighbors = get_neighbors(input_grid, row, col)

            # Apply the transformation rule
            if current_color == 1:  # If the pixel is blue
                if 1 in neighbors:  # and any neighbor is blue
                    output_grid[row, col] = 2  # Change to red

    return output_grid