"""
Identify a specific 2x2 colored square (orange, magenta, maroon, yellow), 
move it down to align with the bottom of the grid, creating a copy, 
and shifting the copy to the right to align with the final column.
Delete the azure(8) square.
"""

import numpy as np

def find_squares(grid):
    squares = []
    for r in range(len(grid) - 1):
        for c in range(len(grid[0]) - 1):
            if grid[r, c] != 0 and grid[r, c+1] != 0 and grid[r+1, c] != 0 and grid[r+1, c+1] != 0:
                squares.append({
                    "top_left": (r, c),
                    "colors": (grid[r, c], grid[r, c+1], grid[r+1, c], grid[r+1, c+1])
                })
    return squares

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all 2x2 squares
    squares = find_squares(input_grid)

    # Target square and new locations
    target_colors = (7, 6, 9, 4)
    target_square = None

    for square in squares:
      if square["colors"] == target_colors:
        target_square = square
        break

    #Move and duplicate target, if found.
    if target_square:
        # first copy
        row_offset = output_grid.shape[0] - 2 - target_square["top_left"][0]
        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1]] = 7
        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1] + 1] = 6
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1]] = 9
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1] + 1] = 4
        # second copy
        col_offset = output_grid.shape[1] - 2 - target_square["top_left"][1]

        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1] + col_offset ] = 7
        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1] + 1 + col_offset] = 6
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1] + col_offset] = 9
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1] + 1 + col_offset] = 4

    return output_grid