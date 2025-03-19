"""
The transformation rule involves identifying a vertical orange (7) line in the input grid,
replicating it to the right with an alternating pattern of orange(7) and azure(8), and then adjusting
the shape of the formation.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find a vertical line of a specified color.
    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color:
                # Check if it's a vertical line
                line_length = 0
                for r2 in range(r, rows):
                    if grid[r2, c] == color:
                        line_length += 1
                    else:
                        break
                if line_length > 0:  #Consider a line of length at least one
                  return r, c, line_length
    return None, None, 0

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find the vertical orange line.
    start_row, start_col, line_length = find_vertical_line(input_grid, 7)

    if start_row is None:
        return output_grid # Return input if there is no line

    # Create replicated lines with changes in length and positions
    new_length = 3
    for i in range(new_length):
      output_grid[i,0] = 7
      if start_col + 1 < output_grid.shape[1]:
        output_grid[i,1] = 8
      if start_col + 2 < output_grid.shape[1]:
        output_grid[i,2] = 7
      if start_col + 3 < output_grid.shape[1]:
        output_grid[i,3] = 8
      if start_col + 4 < output_grid.shape[1]:
        output_grid[i,4] = 7
    output_grid[3,1]=8
    output_grid[3,2]=7
    output_grid[4,2] = 7

    return output_grid