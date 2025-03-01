"""
The transformation rule involves checking for the presence of a blue pixel in the input grid. If no blue pixel is found, the output is an all-zero grid. If a blue pixel is present, its column index is incremented by one to determine the column in the output grid that will be entirely filled with blue pixels.
"""

import numpy as np

def find_blue_pixel(grid):
    # Find the coordinates of the blue pixel (value 1).
    for r in range(grid.shape[0]):
      for c in range(grid.shape[1]):
        if grid[r][c] == 1:
          return (r,c)
    return None

def transform(input_grid):
    # Initialize the output grid with the same dimensions and all zeros.
    output_grid = np.zeros_like(input_grid)

    # find blue, could be none
    blue_pixel = find_blue_pixel(input_grid)

    # if no blue, return all white
    if blue_pixel==None:
      return output_grid

    # get the column of the blue pixel
    blue_col = blue_pixel[1]

    # output column
    output_col = blue_col + 1

    # check output column is in range, otherwise don't add any blue
    if output_col < output_grid.shape[1]:
      # populate all rows of column x with blue
      for row in range(output_grid.shape[0]):
          output_grid[row, output_col] = 1

    return output_grid