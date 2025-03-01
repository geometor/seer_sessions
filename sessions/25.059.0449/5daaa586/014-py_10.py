"""
1.  **Identify Key Lines:** Find the vertical blue (1) line, the horizontal light blue (8) line at row index 2, the horizontal pink (6) line immediately above an all-black (0) row, and the vertical yellow (4) line.

2.  **Define Sub-grid:** Define a sub-grid. The top edge is the light blue (8) row. The bottom edge is the pink (6) row. The left edge is the yellow (4) column. The right edge is the blue (1) column.

3.  **Create Output:** Create the output grid by copying the defined sub-grid.

4.  **Modify Sub-grid:** Within the copied sub-grid, iterate through all pixels. If a pixel's color is not light blue (8), and it falls between the yellow and blue columns (inclusive of yellow, exclusive of blue), change its color to black (0).
"""

import numpy as np

def find_color_line(grid, color, orientation):
    """Finds the first line (row or column) of a given color.

    Args:
      grid: The input grid (NumPy array).
      color: The color to search for.
      orientation: 'horizontal' or 'vertical'.

    Returns:
      The index of the first row or column containing only the color, or -1 if not found.
    """
    if orientation == 'horizontal':
        for i, row in enumerate(grid):
            if np.all(row == color):
                return i
        return -1
    elif orientation == 'vertical':
        for j in range(grid.shape[1]):
            if np.all(grid[:, j] == color):
                return j
        return -1
    else:
      return -1

def find_color_column(grid, color):
    """Finds the first occurence of a column of a specified color"""
    for j in range(grid.shape[1]):
      if np.all(grid[:, j] == color):
          return j
    return -1

def find_pink_row(grid):
    """Find the horizontal line of '6' (pink) above the first all '0's row"""
    for i in range(grid.shape[0]-1):
        if np.all(grid[i,:] == 6) and np.all(grid[i+1,:]==0):
            return i;
    return -1


def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Convert input to NumPy array
    input_grid = np.array(input_grid)

    # 1. Identify Key Columns and Rows
    blue_column_index = find_color_column(input_grid, 1)
    light_blue_row_index = find_color_line(input_grid, 8, 'horizontal')
    pink_row_index = find_pink_row(input_grid)
    yellow_column_index = find_color_column(input_grid, 4)


    # 2. Extract Sub-grid
    top = light_blue_row_index
    bottom = pink_row_index
    left = yellow_column_index
    right = blue_column_index

    if top is None or bottom is None or left is None or right is None:
      return input_grid.tolist()
    if -1 in [top, bottom, left, right]:
        return input_grid.tolist()
    sub_grid = input_grid[top:bottom+1, left:right+1]

    # 3. Output Generation: Copy the sub-grid
    output_grid = sub_grid.copy()

    # 4. Modify Sub-grid
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            # Check if the pixel is within the yellow-blue range (inclusive of yellow, exclusive of blue)
            # and if it's not light blue (8)
            if 0 <= j < right - left and output_grid[i, j] != 8:
                output_grid[i, j] = 0

    return output_grid.tolist()