"""
Replaces white (0) pixels in the input grid with blue (1) pixels based on their surrounding neighbors. Other colored pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the 8 neighbors (including diagonals) of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):  # Exclude the pixel itself
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """Transforms the input grid by changing some white pixels to blue."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels
    for row in range(rows):
        for col in range(cols):
            # Check for white pixels
            if input_grid[row, col] == 0:
                # Get neighbors
                neighbors = get_neighbors(input_grid, row, col)
                
                output_grid[row,col] = 1 # change the current cell to 1

    return output_grid