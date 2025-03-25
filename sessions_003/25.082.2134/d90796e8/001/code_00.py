"""
Red pixels that are next to green pixels become azure pixels. All other pixels remain unchanged.
"""

import numpy as np

def is_adjacent_or_diagonal(coord1, coord2):
    """
    Checks if two coordinates are adjacent or diagonal.

    Args:
      coord1: Tuple (row1, col1)
      coord2: Tuple (row2, col2)

    Returns:
      True if adjacent or diagonal, False otherwise.
    """
    row_diff = abs(coord1[0] - coord2[0])
    col_diff = abs(coord1[1] - coord2[1])
    return row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff > 0)


def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Red pixels adjacent or diagonal to green pixels become azure.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        for j in range(cols):
            # Check if the current cell is red
            if input_grid[i, j] == 2:
                # Check neighbors for green
                for x in range(max(0, i - 1), min(rows, i + 2)):
                    for y in range(max(0, j - 1), min(cols, j + 2)):
                        if (x != i or y != j) and input_grid[x, y] == 3: # Found adjacent Green
                            output_grid[i,j] = 8

    return output_grid