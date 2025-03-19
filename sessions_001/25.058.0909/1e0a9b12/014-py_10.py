"""
Shifts non-zero colored cells in a grid downwards, maintaining their x-coordinate (column),
and stacks them at the bottom of the grid in the original order of top to bottom, left to right.
"""

import numpy as np

def get_nonzero_cells(grid):
    """Finds and returns non-zero cells with their original row and column indices."""
    nonzero_cells = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                nonzero_cells.append((r, c, grid[r, c]))
    return nonzero_cells

def transform(input_grid):
    """Transforms the input grid by shifting non-zero cells down."""
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Get non-zero cells from input, keeping initial locations.
    nonzero_cells = get_nonzero_cells(input_grid)

    # sort by row, then column
    nonzero_cells.sort(key=lambda x: (x[0], x[1]))

    # compute new locations, starting at bottom
    num_rows = input_grid.shape[0]
    current_row = num_rows-len(nonzero_cells)

    for _, col, value in nonzero_cells:
        output_grid[current_row,col] = value
        current_row += 1

    return output_grid