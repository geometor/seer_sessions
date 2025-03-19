"""
Selects columns 0 and 2 (zero-indexed) from the input grid and constructs a new grid from these columns, preserving the original row order and values.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by selecting specific columns.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid)
    rows = input_grid.shape[0]
   
    # select input columns
    selected_columns = [0, 2]

    #check if columns exist
    cols = input_grid.shape[1]
    for col_index in selected_columns:
      if col_index >= cols:
          return input_grid.tolist() # or some other default behavior, like an empty grid


    # build output by gathering selected input columns
    output_grid = input_grid[:, selected_columns]

    return output_grid.tolist()