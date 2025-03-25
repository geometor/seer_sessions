"""
The transformation extracts the leftmost non-zero pixel from each row of the shape created by the non-zero pixels in the input. The output grid's size will change based on how tall the shape is.
"""

import numpy as np

def get_active_region(grid):
    # returns the rows containing non-zero elements
    rows = []
    for i, row in enumerate(grid):
      if any(val != 0 for val in row):
        rows.append(i)
    return rows

def transform(input_grid):
    # convert to numpy array
    input_grid = np.array(input_grid)

    # Identify rows with Non-Zero Pixels
    active_rows = get_active_region(input_grid)

    # create output grid
    output_grid = []
    # Iterate Top to Bottom Rows of active region
    for row_index in active_rows:
      row = input_grid[row_index]

      # Extract Leftmost non-zero Pixel in Row
      for pixel in row:
        if pixel != 0:
          output_grid.append(pixel)
          break # only take first one

    # shape output
    output_grid = np.array(output_grid).reshape(-1,3)

    return output_grid