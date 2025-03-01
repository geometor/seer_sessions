"""
A diagonal line of green (3) pixels is drawn, starting at a position that is dynamically determined based on grid and objects. The line extends downwards and to the right (one column per row). The green line stops one row *above* the *top* of either an azure (8) object *or* a red (2) object, whichever is encountered *first* vertically. If neither a red nor azure pixel exists below the line, the green line fills down to the end of the grid. The red and azure objects remain unchanged.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def get_stopping_row(input_grid, start_col):
    """
    Calculates the row index where the green line should stop.
    Considers both red (2) and azure (8) objects.
    Returns the row index *above* the first obstacle encountered.
    """
    rows, cols = input_grid.shape
    red_pixels = find_object_by_color(input_grid, 2)
    azure_pixels = find_object_by_color(input_grid, 8)

    stopping_row = rows  # Default: go to the bottom

    #check for red
    for row in range(rows):
        col = start_col + row
        if col < cols:
            for red_row, red_col in red_pixels:
                if red_row == row + 1 and red_col == col:
                  return row

    # Check for azure pixels below the diagonal
    for row in range(rows):
      col = start_col + row
      if (col < cols):
        for azure_row, azure_col in azure_pixels:
          if (azure_row == row + 1) and (azure_col == col):
            stopping_row = row # Found azure pixel one row below, stop here
            return stopping_row

    return stopping_row

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Determine the starting column.  Try a few options near the center,
    # and on the left, and adjust based on the presence of obstacles.
    start_col = cols // 2

    # calculate stop row
    stop_row = get_stopping_row(input_grid, start_col)

    # Draw the diagonal green line.
    for row in range(stop_row):
        col = start_col + row
        if col < cols:
          output_grid[row, col] = 3

    return output_grid