"""
The transformation rule is as follows:
1. Keep all maroon (9) pixels unchanged.
2. Iterate through all blue (1) pixels in the input grid.
3.  A blue pixel becomes azure if and only if it has only maroon neighbors
    (up, down, right, left, diagonals included).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Returns a list of the values of the 8 neighbors of a cell (up, down, left, right, and diagonals).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                neighbors.append(grid[i, j])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the rule.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid.
    for row in range(rows):
        for col in range(cols):
            # Check if the current cell is blue (1).
            if input_grid[row, col] == 1:
                # Get the neighbors of the current cell.
                neighbors = get_neighbors(input_grid, row, col)
                # Check if all neighbors are maroon (9).
                if all(neighbor == 9 for neighbor in neighbors):
                    # If all neighbors are maroon, change the cell to azure (8).
                    output_grid[row, col] = 8

    # Return the transformed grid.
    return output_grid