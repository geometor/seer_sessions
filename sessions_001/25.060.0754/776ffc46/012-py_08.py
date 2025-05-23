"""
A blue pixel is transformed to a green pixel if and only if it is a single, isolated pixel (i.e., it is not part of a larger blue object and doesn't have blue neighbors).
"""

import numpy as np

def is_isolated(grid, r, c, color):
    """
    Checks if a pixel at (r, c) of the given color is isolated (has no neighbors of the same color).
    """
    rows, cols = len(grid), len(grid[0])

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself

            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == color:
                return False  # Found a neighbor of the same color

    return True

def transform(input_grid):
    """
    Transforms the input grid by changing isolated blue pixels to green.

    Args:
        input_grid (numpy.ndarray): The input grid.

    Returns:
        numpy.ndarray: The transformed grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid and change isolated blue (1) pixels to green (3).
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 1 and is_isolated(output_grid, r, c, 1):
                output_grid[r, c] = 3

    return output_grid