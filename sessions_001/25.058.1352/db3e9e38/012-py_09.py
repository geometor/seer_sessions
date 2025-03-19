"""
The transformation rule identifies a vertical orange (7) line in the input,
then generates an inverse 'L' shape using an alternating pattern of orange (7) and azure (8)
pixels, starting from the top of the identified line.
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
    # Initialize output_grid as a copy of input.
    output_grid = np.copy(input_grid)

    # Find the vertical orange line.
    start_row, start_col, line_length = find_vertical_line(input_grid, 7)

    if start_row is None:
        return output_grid # Return input if no orange line is found

    # Determine the height of the inverse L (number of rows in the pattern).
    pattern_height = line_length + 2 if start_row + line_length +2 <= output_grid.shape[0] else line_length

    # Generate the inverse L shape
    for row in range(min(pattern_height, output_grid.shape[0])):
        for col in range(min(pattern_height-row, output_grid.shape[1])):
            if col+start_col < output_grid.shape[1]:
                if (col) % 2 == 0:
                  output_grid[start_row + row, start_col-col] = 7
                else:
                  output_grid[start_row+ row, start_col - col ] = 8
            else:
              if (col) % 2 == 0:
                output_grid[start_row+ row, col ] = 7
              else:
                output_grid[start_row+ row,col ] = 8

    return output_grid