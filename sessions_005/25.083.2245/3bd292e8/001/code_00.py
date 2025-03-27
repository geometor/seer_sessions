"""
The transformation rule identifies pixels with the value 7 in the input grid. If a 7-pixel is adjacent to a 2-pixel (up, down, left, or right), it's replaced with a 3 in the output grid. Otherwise, if a 7 is not near a 2, it's replaced with a 5. All other pixels retain their original values.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the values of the immediate neighbors (up, down, left, right)."""
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
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is a 7
            if input_grid[row, col] == 7:
                # Get the values of the neighbors
                neighbors = get_neighbors(input_grid, row, col)
                # Check if any neighbor is a 2
                if 2 in neighbors:
                    output_grid[row, col] = 3  # Replace with 3
                else:
                    output_grid[row, col] = 5 # replace with 5
    return output_grid