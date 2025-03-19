"""
The transformation rule consistently reduces the width of the input grid. Specifically, the output grid has a width that is one-third the width of the input grid, keeping three consecutive input columns and collapsing them to first one. The height of the grid remains unchanged. The program takes every three consecutive columns from the input grid, looks at first column of each group of three, then creates a new grid consisting of only those first columns.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid dimensions.
    input_height = len(input_grid)
    input_width = len(input_grid[0])
    output_width = input_width // 3
    output_height = input_height
    output_grid = []

    # Iterate through rows to maintain height
    for row_index in range(output_height):
      new_row = []
      #take every third column starting at 0
      for col_index in range(0,input_width,3):
        new_row.append(input_grid[row_index][col_index])
      output_grid.append(new_row)


    return output_grid