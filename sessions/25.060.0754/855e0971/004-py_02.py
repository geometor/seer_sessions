"""
The transformation rule is:
1. Identify the columns containing white (0) pixels.
2. Within each identified column, Duplicate all rows vertically, and replace the duplicated colors with white pixels in the appropriate location.
"""

import numpy as np

def get_columns_with_color(grid, color):
    # Find columns containing a specified color.
    cols = []
    for x in range(grid.shape[1]):
        if np.any(grid[:, x] == color):
           cols.append(x)
    return cols

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find columns with white pixels (color 0).
    white_cols = get_columns_with_color(input_grid, 0)

     # Duplicate rows in the identified columns, replicating the white
    for col in white_cols:
      for row in range(input_grid.shape[0]):
        if input_grid[row,col] == 0:
          output_grid[:,col] = np.concatenate([input_grid[0:row,col], input_grid[0:input_grid.shape[0]-row,col]], axis=0)
          output_grid[:,col] = np.where(output_grid[:,col] !=0, 0, output_grid[:,col])

    return output_grid