"""
Iterate through each cell of the input grid. If a cell is orange (7), check its immediate horizontal and vertical neighbors *in the input grid*. If any of those neighbors are green (3), change the corresponding cell in the *output* grid to green (3). If a cell is not orange, copy its value to the output grid. Finally return the output grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the immediate horizontal and vertical neighbors of a cell.
    Returns a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate through each cell of the input_grid
    for row in range(rows):
        for col in range(cols):
            # check if it's orange (7) in the input grid
            if input_grid[row, col] == 7:
                # check neighbors in the input grid
                neighbors = get_neighbors(input_grid, row, col)
                neighbor_values = [input_grid[r, c] for (r, c) in neighbors]
                # If any neighbor is green (3), replace with green (3) in the output grid
                if 3 in neighbor_values:
                    output_grid[row, col] = 3

    return output_grid