"""
Iterate through each cell of the input grid. If a cell is non-zero, propagate a value downwards. 
The propagated value is determined by neighbors to the right, then left.
Zeros are replaced with the propagated value until the end of the column is reached.
"""

import numpy as np

def get_neighbor_value(grid, row, col):
    """
    Gets the neighbor value to propagate, prioritizing right then left.
    Returns None if no suitable neighbor.
    """
    rows, cols = grid.shape

    #check right
    if col + 1 < cols and grid[row, col + 1] != 0:
            return grid[row, col + 1]

    # Check left
    if col - 1 >= 0 and grid[row, col - 1] != 0:
        return grid[row, col - 1]

    return None

def transform(input_grid):
    """Transforms the input grid according to the propagation rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each cell
    for row in range(rows):
        for col in range(cols):
            # Check if the current cell is non-zero
            if input_grid[row, col] != 0:
                neighbor_value = get_neighbor_value(input_grid, row, col)
                # Propagate downwards
                for r in range(row + 1, rows):
                    if output_grid[r, col] == 0:  # Only replace zeros
                        if neighbor_value is not None:
                          output_grid[r, col] = neighbor_value
                        else:
                          output_grid[r,col] = input_grid[row,col]
                    else:
                        break  # Stop propagation if a non-zero cell is encountered


    return output_grid