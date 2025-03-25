"""
The transformation rule copies the first two rows of the input grid to the output grid. Then, for each subsequent row in the output grid, it iterates through the columns of the input grid. For each column, it takes the corresponding element from the first row and adds it to the current output row. After constructing output with values from first row it does the same with second row. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    input_height, input_width = input_grid.shape
    output_grid = np.copy(input_grid)

    # Copy the first two rows
    #output_grid[0] = input_grid[0]
    #output_grid[1] = input_grid[1]

    # Construct subsequent rows based on column elements of the first two rows
    for i in range(2, input_height):
      row_index = i % 2  # 0 for first row, 1 for second row
      new_row = []
      for j in range(input_width):
        new_row.append(input_grid[row_index, j])
      output_grid[i] = new_row
    return output_grid