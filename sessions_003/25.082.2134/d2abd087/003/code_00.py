"""
Transforms an input grid by changing the color of gray (5) pixels to either red (2) or blue (1) based on their position and neighbors, creating a checkerboard pattern of connected gray pixel islands. The color assignment is done *during* the flood fill operation, avoiding a second pass.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a pixel (including diagonals)."""
    rows, cols = len(grid), len(grid[0])
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append((i, j))
    return neighbors

def flood_fill(grid, row, col, target_color, replacement_color, visited):
    """Performs a flood fill operation, directly applying the replacement color."""
    rows, cols = len(grid), len(grid[0])
    if (row < 0 or row >= rows or col < 0 or col >= cols or
            (row, col) in visited or grid[row][col] != target_color):
        return
    visited.add((row, col))
    grid[row][col] = replacement_color

    neighbors = get_neighbors(grid, row, col)
    for r, c in neighbors:
        flood_fill(grid, r, c, target_color, replacement_color, visited)

def transform(input_grid):
    # Initialize output_grid as a *copy* of the input
    output_grid = np.copy(input_grid).tolist()
    rows, cols = len(output_grid), len(output_grid[0])

    # Keep track of visited pixels
    visited = set()

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Process only unvisited gray pixels
            if output_grid[r][c] == 5 and (r, c) not in visited:
                # Determine checkerboard color:
                start_color = 1  # Default to blue
                if (r > 0 and output_grid[r-1][c] == 1) or \
                   (c > 0 and output_grid[r][c-1] == 1):
                    start_color = 2  # change to Red
                elif (r > 0 and output_grid[r-1][c] == 2) or \
                   (c > 0 and output_grid[r][c-1] == 2):
                    start_color = 1 # change to Blue

                # Flood fill with the determined color
                flood_fill(output_grid, r, c, 5, start_color, visited)

    return output_grid