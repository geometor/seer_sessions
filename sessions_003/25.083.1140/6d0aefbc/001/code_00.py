"""
The transformation rule duplicates each column of the input grid to create the output grid. The output grid has the same number of rows as the input grid, but twice the number of columns.
"""

import numpy as np

def transform(input_grid):
    # Get the dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Create the output grid with twice the number of columns
    output_grid = []

    # Iterate over rows to copy
    for row in input_grid:
      new_row = []
      # duplicate pixels
      for pixel in row:
          new_row.append(pixel)
          new_row.append(pixel)
      output_grid.append(new_row)
      

    return output_grid