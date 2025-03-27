"""
Iterates through the input grid, examining vertical pairs of cells.
If the bottom cell's color is not 0, and is different than the cell directly above, 
the color of the cell above is changed to match the bottom cell.
This propagation continues upwards until the edge of the grid is reached
or a cell with the same color, or is not a different color, is encountered.
"""

import numpy as np

def get_vertical_pairs(grid):
    """Extracts all vertically adjacent pairs of cells."""
    pairs = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols):
            pairs.append( ((r, c), (r + 1, c)) )
    return pairs

def propagate_color(grid, row, col, color):
    """Propagates the given color upwards from the given position."""
    # output_grid is a copy, we modify this
    while row >= 0 and grid[row,col] != color:
        grid[row, col] = color
        row -= 1

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # get all vertical pairs - iterate from top down
    pairs = get_vertical_pairs(input_grid)

    # loop through pairs for replacement
    for (top_row, top_col), (bottom_row, bottom_col) in pairs:
        top_color = input_grid[top_row, top_col]
        bottom_color = input_grid[bottom_row, bottom_col]

        # change output pixels
        if bottom_color != 0 and top_color != bottom_color:
            propagate_color(output_grid, top_row, top_col, bottom_color)

    return output_grid