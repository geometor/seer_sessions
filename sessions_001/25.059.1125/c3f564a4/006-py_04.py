"""
The transformation rule is to identify '0' (white) pixels within a repeating "1 2 3 4 5" sequence in a grid, and replace them with the correct number of the sequence, maintaining the pattern horizontally and vertically.
"""

import numpy as np

def get_expected_value(grid, row, col):
    """
    Determines the expected value of a cell based on its neighbors,
    considering the repeating 1-5 sequence.
    """
    rows, cols = grid.shape
    neighbors = []

    # Check neighbors (up, down, left, right)
    if row > 0:
        neighbors.append(grid[row - 1, col])
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])
    if col > 0:
        neighbors.append(grid[row, col - 1])
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])

    # Determine expected value based on neighbors, handling wrapping
    for neighbor in neighbors:
        if neighbor != 0:
            expected = (neighbor % 5) + 1
            #check wrapped condition
            if expected == 6:
                expected = 1
            
            #check if expected number creates valid sequence
            if row > 0 and grid[row-1][col] != 0:
                if (grid[row-1][col] % 5) + 1 != expected and grid[row-1][col] != expected:
                    continue
            if row < rows - 1 and grid[row+1][col] != 0:
                if (grid[row+1][col] % 5) + 1 != expected and grid[row + 1][col] != expected:
                    continue
            if col > 0 and grid[row][col-1] != 0:
                if (grid[row][col-1] % 5 ) + 1 != expected and grid[row][col - 1] != expected:
                    continue
            if col < cols - 1 and grid[row][col + 1] != 0:
                if (grid[row][col+1] % 5) + 1 != expected and grid[row][col+1] != expected:
                    continue

            return expected

    return 0 # Should not reach this in a valid pattern.


def transform(input_grid):
    """
    Transforms the input grid by replacing '0' pixels with the appropriate
    value from the repeating sequence "1 2 3 4 5".
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell in the grid
    for i in range(rows):
        for j in range(cols):
            if output_grid[i][j] == 0:
                # Determine the expected value based on neighbors
                expected_value = get_expected_value(output_grid, i, j)
                output_grid[i][j] = expected_value

    return output_grid