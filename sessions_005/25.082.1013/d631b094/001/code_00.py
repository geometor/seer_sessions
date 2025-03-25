"""
1. Identify the single non-zero color (pixel value) present in the input grid.
2. Count the number of times the non-zero color appears in the rows and/or columns of the input grid, OR count the number of rows and/or columns that contain it. It's unclear at this stage if counting by element or by row/col, more examples needed to know for sure.
3.  Determine the dimensions of output. Number of non-zero values on each row, or number of rows containing non zero values, or some combination. More examples are needed to discern this.
4. Create an output grid consisting solely of the identified non-zero color, repeated according to calculated dimension above.
"""

import numpy as np

def get_nonzero_color(grid):
    """
    Finds and returns the single non-zero color in a grid.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    return 0  # Return 0 if no non-zero color is found

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    non_zero_color = get_nonzero_color(input_grid)

    if non_zero_color == 0:
      return []
    
    rows_with_color = 0
    for row in input_grid:
      if non_zero_color in row:
          rows_with_color +=1

    cols_with_color = 0
    for col in input_grid.T:
      if non_zero_color in col:
          cols_with_color += 1

    output_grid_dimension = rows_with_color * cols_with_color - (rows_with_color + cols_with_color - np.count_nonzero(input_grid)) #best guess so far

    output_grid = np.full(output_grid_dimension, non_zero_color)

    return output_grid.tolist()