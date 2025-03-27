"""
Counts the number of corners and adjacent same color tiles in a 3x3 grid.
"""

import numpy as np

def count_corners_and_adjacent(grid):
    """
    Counts corners with adjacent same-color tiles.
    """
    grid = np.array(grid)
    if grid.shape != (3, 3):
        return 0  # Not a 3x3 grid

    count = 0

    # Check top-left corner
    if grid[0, 0] != 0:
      if grid[0,0] == grid[0,1]:
        count += 1
      if grid[0,0] == grid[1,0]:
        count += 1

    # Check top-right corner
    if grid[0, 2] != 0:
      if grid[0,2] == grid[0,1]:
        count += 1
      if grid[0,2] == grid[1,2]:
        count += 1

    # Check bottom-left corner
    if grid[2, 0] != 0:
        if grid[2,0] == grid[1,0]:
            count +=1
        if grid[2,0] == grid[2,1]:
            count += 1

    # Check bottom-right corner
    if grid[2, 2] != 0:
        if grid[2,2] == grid[2,1]:
            count += 1
        if grid[2,2] == grid[1,2]:
            count += 1
    return count


def transform(input_grid):
    """
    Counts corners and adjacent tiles of the same color
    """
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Count corners with adjacent same-color tiles
    count = count_corners_and_adjacent(grid)

    return count