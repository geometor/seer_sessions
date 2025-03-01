"""
1.  **Identify Key Lines:** Find the vertical line of color '1' (blue) in the input grid. Find the horizontal line of '8' (light blue) at row index 2. Find the horizontal line of '6' (pink) at the row immediately above a row that is all '0's. Find the vertical line of '4' (yellow) at the third column.

2.  **Define Sub-grid:** Define the sub-grid with the top edge at the '8' row and the bottom edge at the '6' row. The right edge of the subgrid is the column of '1's and the left edge is the column of '4's.

3. **Create Output:** Generate the output grid. Create a copy of the
   input sub-grid. Iterate through the sub-grid copy, replace all
   pixels in the 2nd, 3rd, 4th and 5th columns with 0, unless the original sub-grid value
   is '8'.
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
    return - 1

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

    # 3. Output Generation
    output_grid = sub_grid.copy()

    for i in range(output_grid.shape[0]):
      for j in range(output_grid.shape[1]):
        if j in [1,2,3,4] and output_grid[i,j]!=0:  # Corrected indices 2nd, 3rd, 4th, 5th columns are 1,2,3,4
           output_grid[i,j] = output_grid[i,j] if output_grid[i,j] == 8 else 0

    return output_grid.tolist()