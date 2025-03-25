"""
Iterate through each cell of the input grid. If a cell is orange (7) and
touches the edge of the grid, change it to gray (5). All other cells
retain their original colors.
"""

import numpy as np

def is_edge(grid, row, col):
    """
    Checks if a given cell (row, col) is on the edge of the grid.
    """
    rows, cols = grid.shape
    return row == 0 or row == rows - 1 or col == 0 or col == cols - 1
    

def transform(input_grid):
    """
    Transforms the input grid according to the defined rule.
    """
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through each cell of the grid
    for row in range(rows):
        for col in range(cols):
            # Check if cell is orange and on an edge
            if output_grid[row, col] == 7 and is_edge(output_grid, row, col):
                    # Change to gray
                    output_grid[row, col] = 5

    return output_grid