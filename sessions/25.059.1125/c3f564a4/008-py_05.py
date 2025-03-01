"""
The transformation rule is to identify existing sequences of numbers (1-5) in the grid and extend them to adjacent '0' (white) cells. The sequence wraps around, so after 5 comes 1. Only '0' cells directly adjacent to existing sequence elements are modified.
"""

import numpy as np

def get_expected_value(grid, row, col):
    """
    Determines the expected value of a cell based on its neighbors,
    considering the repeating 1-5 sequence and wrapping.
    """
    rows, cols = grid.shape
    neighbors = []

    # Check neighbors (up, down, left, right)
    if row > 0:
        neighbors.append((row - 1, col, grid[row - 1, col]))
    if row < rows - 1:
        neighbors.append((row + 1, col, grid[row + 1, col]))
    if col > 0:
        neighbors.append((row, col - 1, grid[row, col - 1]))
    if col < cols - 1:
        neighbors.append((row, col + 1, grid[row, col + 1]))

    # Determine expected value based on neighbors
    for r, c, neighbor in neighbors:
        if neighbor != 0:
            expected = (neighbor % 5) + 1
            return expected

    return 0  # Return 0 if no valid adjacent sequence element


def transform(input_grid):
    """
    Transforms the input grid by extending existing 1-5 sequences to adjacent '0' cells.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] == 0:
                # Determine the expected value based on adjacent neighbors
                expected_value = get_expected_value(output_grid, i, j)
                if expected_value != 0:
                     output_grid[i][j] = expected_value

    return output_grid