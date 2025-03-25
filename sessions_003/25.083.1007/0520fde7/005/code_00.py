"""
1.  **Identify the Gray Column:** Find the column index in the input grid containing the gray (5) pixel.
2.  **Check for Blue Pixels:** For each row, check if there's a blue (1) pixel immediately to the left or right of the gray column.
3.  **Determine output width:** If a blue pixel exists to left and/or right, then the output columns should reflect this by adding a column for each.
4.  **Create Output:** Create an output grid. The output should include a column of red pixels for each column left/right that contains a blue pixel, where row index matches. All other pixels should be white (0).
"""

import numpy as np

def find_gray_column(grid):
    """Finds the index of the column containing gray (5)."""
    for j in range(grid.shape[1]):
        if 5 in grid[:, j]:
            return j
    return -1

def find_blue_neighbors(grid, gray_column_index):
    """Finds rows with blue pixels immediately left or right of the gray column."""
    blue_left_rows = []
    blue_right_rows = []
    for i in range(grid.shape[0]):
        if gray_column_index > 0 and grid[i, gray_column_index - 1] == 1:
            blue_left_rows.append(i)
        if gray_column_index < grid.shape[1] - 1 and grid[i, gray_column_index + 1] == 1:
            blue_right_rows.append(i)
    return blue_left_rows, blue_right_rows

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # Find gray column
    gray_column_index = find_gray_column(input_grid)

    if gray_column_index == -1:
        return np.zeros((input_grid.shape[0], 0), dtype=int)

    # Find rows with blue pixels to the immediate left and right
    blue_left_rows, blue_right_rows = find_blue_neighbors(input_grid, gray_column_index)

    # Determine output width and create output grid
    output_width = 0
    if len(blue_left_rows) > 0:
        output_width += 1
    if len(blue_right_rows) > 0:
        output_width += 1

    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)


    # Fill output grid based on blue neighbors
    left_col_index = 0
    
    if len(blue_left_rows) > 0 :
      for row in blue_left_rows:
          output_grid[row, 0] = 2
      if len(blue_right_rows) > 0:
          left_col_index = 1

    if len(blue_right_rows) > 0:
      for row in blue_right_rows:
        output_grid[row,left_col_index] = 2

    return output_grid