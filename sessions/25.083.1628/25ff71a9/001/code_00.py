"""
1. Identify any horizontal lines of the length of the grid composed of non-white color.
2. Move the identified horizontal lines down by one row index.
3. All cells above the original line, which are vacated by the shift are turned into white.
"""

import numpy as np

def find_horizontal_lines(grid):
    # Find non-white horizontal lines of the full grid width
    lines = []
    rows, cols = grid.shape
    for i in range(rows):
        first_pixel = grid[i,0]
        if first_pixel != 0 and np.all(grid[i] == first_pixel):
            lines.append((i, first_pixel))
    return lines

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Find horizontal lines
    lines = find_horizontal_lines(input_grid)
  

    # Move lines down and fill above with white
    for line_index, color in lines:
        new_row_index = line_index + 1
        if new_row_index < rows:
            output_grid[new_row_index, :] = color
        # else the line moves out of grid

    return output_grid