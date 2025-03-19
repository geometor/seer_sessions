"""
The transformation identifies the unique row in the input grid that contains azure (8) pixels and replaces those azure pixels with gray (5) pixels.
"""

import numpy as np

def find_row_with_color(input_grid, color):
    """
    Finds the index of the unique row containing a specified color.
    Returns -1 if the color appears in multiple rows or no rows.
    """
    rows_with_color = []
    for i, row in enumerate(input_grid):
        if color in row:
            rows_with_color.append(i)
    if len(rows_with_color) == 1:
        return rows_with_color[0]
    else:
        return -1


def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = [row[:] for row in input_grid]
    
    # find the unique row with azure pixels
    azure_row_index = find_row_with_color(input_grid, 8)

    # if no such unique row exists, return the original grid
    if azure_row_index == -1:
        return output_grid

    # iterate through the identified row and replace azure with gray
    for i in range(len(output_grid[azure_row_index])):
      if output_grid[azure_row_index][i] == 8:
        output_grid[azure_row_index][i] = 5

    return output_grid