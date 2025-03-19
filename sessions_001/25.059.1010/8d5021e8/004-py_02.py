"""
The transformation rule involves expanding the input grid to create an output grid. The output grid's height is three times the input grid's height, and its width is twice the input grid's width. Azure (8) pixels in the input are replicated vertically to form the border of output. White (0) pixels are expanded to create white row between the border.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for x in range(input_width):
      # find first and last azure in column
      azure_y = []
      for y in range(input_height):
        if input_grid[y,x] == 8:
            azure_y.append(y)

      # copy entire columns where azure was found
      if len(azure_y) > 0:
        for y in range(output_height):
          output_grid[y, x*2] = 8

    # fill every other horizontal line
    for y in range(output_height):
      if y % 3 == 1:
        output_grid[y,:] = 0
      if y % 3 == 2:
        output_grid[y,:] = 0
      if y % 3 == 0:
        for x in range(output_width):
          if output_grid[y,x] != 8:
            output_grid[y,x] = 0

    return output_grid