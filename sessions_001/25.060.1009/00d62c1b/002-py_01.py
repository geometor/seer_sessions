"""
The transformation rule identifies contiguous regions of green (3) pixels.
For each green pixel, it checks for adjacent green pixels. If a green pixel
is surrounded on two or more sides (not diagonally) by other green pixels,
it changes the green pixel to yellow (4). All other pixels remain unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell in the grid."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell in the grid.
    for row in range(rows):
        for col in range(cols):
            # Process only green pixels.
            if input_grid[row, col] == 3:
                neighbor_count = 0
                # Count green neighbors
                for r, c in get_neighbors(input_grid, row, col):
                    if input_grid[r,c] == 3:
                        neighbor_count += 1

                if neighbor_count >= 2:
                    output_grid[row,col] = 4
                

    return output_grid