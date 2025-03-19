"""
The output grid is a 3x3 grid. It is constructed by finding a vertical line of
identical, non-zero colored pixels in the input grid.  The top of this line
is the upper-left corner of the output grid, and the line extends diagonally down
and to the right. If multiple such lines exist, the one with the greatest
y-coordinate is used, and if ties still exist, the one with the smallest
x-coordinate is used.
"""

import numpy as np

def find_diagonal_line_start(grid):
    """Finds the starting position of the diagonal line."""
    grid = np.array(grid)
    rows, cols = grid.shape
    best_start = None

    for r in range(rows - 1, -1, -1):  # Start from the bottom
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and r + 1 < rows and c + 1 < cols and grid[r+1, c] == 0 and grid[r+1,c+1] == color:
                if best_start is None or r > best_start[0]: # or (r == best_start[0] and c < best_start[1]):
                    best_start = (r, c)
    return best_start

def transform(input_grid):
    # Find the starting position of the diagonal line.
    start_pos = find_diagonal_line_start(input_grid)

    # initialize to 3x3 of all zeros
    output_grid = np.zeros((3,3),dtype=int)

    # If no diagonal line found, return all zeros
    if start_pos is None:
        return output_grid.tolist()

    # construct the output
    input_array = np.array(input_grid)
    r,c = start_pos
    color = input_array[r,c]

    output_grid[0,0] = color
    if r + 1 < input_array.shape[0] and c + 1 < input_array.shape[1]:
        output_grid[1,1] = color
    if r + 2 < input_array.shape[0] and c + 2 < input_array.shape[1]:
        output_grid[2,2] = color

    return output_grid.tolist()