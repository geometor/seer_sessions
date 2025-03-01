"""
The transformation rule is as follows:

1.  Identify two objects within the grid: a red object (color 2) and an azure object (color 8).
2.  The azure object (color 8) remains in its original position.
3.  The red objects shape and position in the input becomes empty in the output.
4.  The shape of the red object is identified in the input.
5.  A copy of the shape of the red object appears on the grid, such that the top two rows overlap the initial position of the red object.

"""

import numpy as np

def find_object(grid, color):
    """Finds the coordinates of an object of the specified color."""
    coords = np.argwhere(grid == color)
    return coords

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Find the red and azure objects.
    red_coords = find_object(input_grid, 2)
    azure_coords = find_object(input_grid, 8)

    # clear initial red object position
    for r, c in red_coords:
        output_grid[r, c] = 0

    #  azure object remains in its original position (copy it to the output).

    # Determine the shift.  top two rows of initial position overlaps with the
    # new position
    if len(red_coords) > 0 :
      min_red_row = np.min(red_coords[:, 0])
      # shift_rows = 5
      new_red_coords = []
      # add object to new position
      for r, c in red_coords:
        # new_row = r + shift_rows
        new_row = r + (min_red_row + (min_red_row - r))
        new_red_coords.append( (new_row,c))
        output_grid[new_row, c] = 2

    return output_grid