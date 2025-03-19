"""
The transformation rule is:
1. Identify White Regions: Locate the vertical columns in the input grid that contain white pixels (0).
2. Vertical Reflection: For each column containing white, reflect the input grid vertically.
3. Reflection Axis: The vertical reflection point is implicitly defined. The reflection includes all rows of the input, and adds rows until the white region is duplicated in size.
"""

import numpy as np

def get_columns_with_color(grid, color):
    """Finds columns containing a specified color."""
    cols = []
    for x in range(grid.shape[1]):
        if np.any(grid[:, x] == color):
           cols.append(x)
    return cols

def transform(input_grid):
    """Transforms the input grid according to the identified rule."""
    input_grid = np.array(input_grid)  # Ensure input is a NumPy array
    # Find columns with white pixels (color 0).
    white_cols = get_columns_with_color(input_grid, 0)

    output_grid = np.copy(input_grid)

    # Vertical Reflection for columns with white
    for col in white_cols:
        # Find the contiguous white region in the column
        white_indices = np.where(input_grid[:, col] == 0)[0]
        if len(white_indices) > 0:
          white_start = white_indices[0]
          white_end = white_indices[-1]
          white_height = white_end-white_start + 1

          #create a slice of the input to reflect
          reflect_region = input_grid[0:white_end+1, col]
          
          #create an extended output grid
          new_height = input_grid.shape[0] + white_height
          output_grid = np.zeros((new_height, input_grid.shape[1]), dtype=int)

          #copy original input to new grid
          output_grid[0:input_grid.shape[0],:] = input_grid

          #add reflected region
          output_grid[white_end + 1: white_end+1+reflect_region.shape[0], col] = reflect_region

    return output_grid