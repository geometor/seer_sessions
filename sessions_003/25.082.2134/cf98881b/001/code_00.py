"""
Transformation Rule:

1. Locate the first occurrence of the digit '2' (red) in the input grid.
2. Extract the four columns up to and including the column where '2' first appears.
3. If '2' is within the first four columns, extract those columns.
4. Extract the first four rows of the input grid.
5. Construct a 4x4 output grid from the intersection of the extracted rows and columns.
6. Handle cases where there are fewer than four columns to the left by potentially wrapping around, although the exact wrapping logic requires further refinement.

"""

import numpy as np

def find_first_occurrence(grid, value):
    # Find the row and column indices of the first occurrence of a value in the grid.
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == value:
                return i, j
    return None, None  # Value not found


def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((4, 4), dtype=int)

    # Find the first occurrence of '2'.
    _, col_index = find_first_occurrence(input_grid, 2)

    # Determine the start and end column indices for extraction
    if col_index is not None:
      start_col = max(0, col_index - 3)
      end_col = col_index +1
    
    else:
       start_col = 0
       end_col = 4

    
    # Extract the relevant rows and columns, and construct the output grid.

    selected_cols = []
    
    current_col = start_col
    
    while len(selected_cols) < 4:
       selected_cols.append(current_col % cols)
       current_col += 1

    for i in range(min(4,rows)):
      for j in range(len(selected_cols)):
          output_grid[i][j] = input_grid[i][selected_cols[j]]

    return output_grid.tolist()