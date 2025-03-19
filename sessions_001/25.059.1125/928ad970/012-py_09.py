"""
Identifies blue objects, expands them by one layer into adjacent white cells only, and preserves all other colored pixels.
"""

import numpy as np

def find_blue_pixels(grid):
    # Find coordinates of all blue pixels.
    rows, cols = np.where(grid == 1)
    return list(zip(rows, cols))

def get_neighbors(grid, row, col):
    # Get the valid neighbors (up, down, left, right) of a cell.
    neighbors = []
    rows, cols = grid.shape
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
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.array(input_grid).copy()
    input_grid = np.array(input_grid)

    # Find all blue pixels
    blue_pixels = find_blue_pixels(input_grid)

    # Expand blue pixels by one layer, but only into white cells
    for row, col in blue_pixels:
        neighbors = get_neighbors(input_grid, row, col)
        for n_row, n_col in neighbors:
            if input_grid[n_row, n_col] == 0:  # Check if the neighbor is white
                output_grid[n_row, n_col] = 1  # Only then, change it to blue

    # Preserve all colors: this is done by default because we started with a copy,
    # and we only modified white cells adjacent to blue cells

    return output_grid.tolist()