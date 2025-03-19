# 5daaa586 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Key Columns and Rows:** Locate the vertical line of color '1' (blue) in the input grid. Locate the horizontal line of '8' (light blue) at row three. Locate the horizontal line of color '6'(pink) at row ten. Locate the vertical line of '4'(yellow) at the third column.

2.  **Extract Sub-grid:** Focus on a sub-grid region. The left border is the column of '4's, the right border is the column of '1'. The upper bound is the row of '8's, the lower bound is the row of '6's.

3.  **Output Generation:** Create the output grid. Maintain every pixel in the sub-grid, replace all other sub-grid pixels in columns 3,4,5,6 with '0'.
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

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Convert input to NumPy array
    input_grid = np.array(input_grid)

    # 1. Identify Key Columns and Rows
    blue_column_index = find_color_column(input_grid, 1)
    light_blue_row_index = find_color_line(input_grid, 8, 'horizontal')
    pink_row_index = find_color_line(input_grid, 6, 'horizontal')
    yellow_column_index = find_color_column(input_grid, 4)


    # 2. Extract Sub-grid
    top = light_blue_row_index
    bottom = pink_row_index
    left = yellow_column_index
    right = blue_column_index
    sub_grid = input_grid[top:bottom+1, left:right+1]

    # 3. Output Generation
    output_grid = sub_grid.copy()

    for i in range(output_grid.shape[0]):
      for j in range(output_grid.shape[1]):
        if j in [2,3,4,5] and output_grid[i,j]!=0:
           output_grid[i,j] = output_grid[i,j] if output_grid[i,j] == 8 else 0

    return output_grid.tolist()
```
