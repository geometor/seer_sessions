"""
Constructs a 4x4 output grid from an input grid divided by a horizontal blue line.

The output grid is initialized with the first four columns of the section above the blue line.
Then, it merges/replaces values column-wise:  If a pixel in the output grid doesn't
match what's expected, we use a value from the same column in the section below the blue
line.
"""

import numpy as np

def find_blue_line(grid):
    """Finds the row index of the horizontal blue line."""
    for i, row in enumerate(grid):
        if all(pixel == 1 for pixel in row):
            return i
    return -1

def transform(input_grid):
    input_grid = np.array(input_grid)
    blue_line_row = find_blue_line(input_grid)
    upper_section = input_grid[:blue_line_row, :4]  # First 4 cols above blue line
    lower_section = input_grid[blue_line_row + 1:]

    # Initialize the output grid (4x4)
    output_grid = np.zeros((4, 4), dtype=int)

    # Initialize with values from the upper section
    for i in range(min(4, upper_section.shape[0])):  # handle short upper
        for j in range(4):
          if upper_section.shape[1] > j:
            output_grid[i, j] = upper_section[i, j]

    # Column-wise merge/replace using lower section, going row by row
    for j in range(4): # columns
      lower_index = 0
      for i in range(4):  # rows
        # see if we have a value to take from the lower section
        if lower_index < lower_section.shape[0]:  # ensure we are within the lower
          output_grid[i,j] = lower_section[lower_index, j]
          lower_index += 1
        # else we keep the initial value from the upper section

    return output_grid.tolist()