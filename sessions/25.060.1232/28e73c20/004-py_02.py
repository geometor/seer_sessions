"""
Transforms an input grid into a grid with a green (3) spiral pattern, starting from the top-left corner and moving inwards.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid to create a green spiral pattern.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    row, col = 0, 0
    dr, dc = 0, 1  # Initial direction: moving right

    def is_valid(r, c, grid):
        #check if row and col are within grid boundary
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    for _ in range(rows * cols):  # Maximum possible steps in the spiral
        if is_valid(row, col, output_grid):
            if output_grid[row, col] == 0: #only change if current cell is white
                output_grid[row, col] = 3

            #check next direction
            next_row, next_col = row + dr, col + dc

            #if the next position is not valid, OR if it is valid and already green, turn
            if not is_valid(next_row, next_col, output_grid) or output_grid[next_row, next_col] == 3:
                #turn right
                dr, dc = dc, -dr # Rotate direction: (0,1)->(1,0)->(0,-1)->(-1,0)
        else:
            break

        row += dr
        col += dc

    return output_grid