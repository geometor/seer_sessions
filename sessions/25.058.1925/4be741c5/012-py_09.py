"""
The transformation rule can be described as follows:

1.  **Iterate** through the input grid based on a pre-defined pattern (either rows or columns, or potentially just the first row/column).
2.  **Extract Unique Colors:** For the selected dimension (row or column or
    first row/column) identify the unique colors present.
3.  **Preserve Order:** Maintain the order of the colors as they first appear
    within the selected dimension.
4. **Construct Output:** create a new grid. If iterating rows, create columns, if
   iterating columns, create rows. If using just the first row/column, then match the
   input dimension.
5. **Populate:** Populate the new grid with the ordered, unique colors.
"""

import numpy as np

def get_unique_colors(data, axis):
    """
    Extracts unique colors along a specified axis, preserving order.
    """
    unique_colors = []
    if axis == 'row':
      for x in data:
        if x not in unique_colors:
          unique_colors.append(x)
    if axis == 'column':
        for x in data:
            if x not in unique_colors:
                unique_colors.append(x)
    return unique_colors

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape

    # Check if we should process rows or columns
    process_rows = False
    process_columns = False
    first_row_only = False
    first_col_only = False

    if rows == cols: # if square, default is to process rows
        process_rows = True
    if rows < cols: # if more cols that rows, process by rows
        process_rows=True
    elif cols < rows:
        process_columns = True

    # determine if only first row, or first col
    if process_rows:
      first_row = input_grid[0,:]
      if len(np.unique(first_row)) == len(first_row): # use first row
          first_row_only = True
      else: # use all rows
          process_rows=True
    elif process_columns: # if process_columns
      first_col = input_grid[:,0]
      if len(np.unique(first_col)) == len(first_col):
        first_col_only = True
      else:
        process_columns=True

    # Initialize output_grid based on processing type
    if first_row_only:
        unique_colors = get_unique_colors(input_grid[0, :], axis='row')
        output_grid = np.array(unique_colors).reshape(1, -1)
    elif first_col_only:
        unique_colors = get_unique_colors(input_grid[:, 0], axis='column')
        output_grid = np.array(unique_colors).reshape(-1, 1)
    elif process_rows:
      # iterate through rows, get unique colors, then stack
      output_data = []
      for i in range(rows):
        row = input_grid[i, :]
        unique = get_unique_colors(row,axis='row')
        output_data.append(unique)
      output_grid = np.array(output_data[0]).reshape(-1,1) # just get first row, for now

    elif process_columns:
      output_data = []
      for j in range(cols):
          col = input_grid[:,j]
          unique = get_unique_colors(col,axis='column')
          output_data.append(unique)
      output_grid = np.array(output_data[0]).reshape(-1,1)

    return output_grid