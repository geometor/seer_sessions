"""
The transformation rule involves creating a 3x6 output grid from an 8x8 input grid. The output grid uses the same two colors as the input. The non-zero elements in the input grid, specifically their row and column positions, determine the content of the output grid. The rows for the output grid is determined by rows with non-zero elements. Output columns are filled with available pixels from the input grid based on non-zero columns.
"""

import numpy as np

def get_nonzero_rows(input_grid):
    """
    Returns a list of unique row indices that contain non-zero elements.
    If a row has multiple non-zero, consider only first one.
    """
    rows = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r, c] != 0:
                rows.append(r)
                break  # Move to next row after first non zero
    return rows

def get_nonzero_cols_every_other(input_grid):
  """
  Return column indices that have non zero element, consider every other column.
  """
  cols = []
  for c in range(0, input_grid.shape[1], 2):
      for r in range(input_grid.shape[0]):
          if input_grid[r, c] != 0:
              cols.append(c)
              break

  return cols

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Initialize output grid
    output_grid = np.zeros((3, 6), dtype=int)

    # Get rows and columns
    non_zero_rows = get_nonzero_rows(input_grid)
    non_zero_cols = get_nonzero_cols_every_other(input_grid)

    # Iterate through output rows
    for output_row in range(3):
        # Determine input row
        input_row_index = output_row % len(non_zero_rows)
        input_row = non_zero_rows[input_row_index]


        # Populate output row
        output_col = 0
        for input_col in range(input_grid.shape[1]):
            if input_grid[input_row, input_col] != 0:
                output_grid[output_row, output_col] = input_grid[input_row, input_col]
                output_col +=1
            if output_col >= 6:
                break
    return output_grid.tolist()