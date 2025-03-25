```python
"""
1.  **Find Gray Column:** Determine the index of the column containing gray (5) in the input grid.
2.  **Create Output Grid:** Create an output grid with the same height as the input grid and a width of 3, initially filled with white (0).
3.  **Locate Blue Pixels:** Identify the rows in input where there are blue pixels (1) in any column, either to the left or right of the identified gray column.
4.  **Transform Adjacent Columns:** For each row containing a blue pixel in any column left or right of the grey column, set the cells in that row to red (2) at the columns immediately to the left and right of the gray column in the output. If there is no column to the left or right (edge case), consider just the available side.
5.  **Fill with White:** Fill all other cells in the output with color white (0).
"""

import numpy as np

def find_gray_column(grid):
    """Finds the index of the column containing gray (5)."""
    for j in range(grid.shape[1]):
        if 5 in grid[:, j]:
            return j
    return -1

def find_blue_rows(grid, gray_column_index):
    """Identifies rows with blue pixels to the left or right of the gray column."""
    blue_rows = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if j != gray_column_index and grid[i,j] == 1:
                blue_rows.append(i)
                break  # Once a blue pixel is found in a row, move to the next row
    return blue_rows
def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # Create output grid (same height, width 3, filled with white)
    output_grid = np.zeros((input_grid.shape[0], 3), dtype=int)

    # Find gray column
    gray_column_index = find_gray_column(input_grid)

    if gray_column_index == -1:
      return output_grid

    # Find rows with blue pixels to the left or right of the gray column
    blue_rows = find_blue_rows(input_grid, gray_column_index)

    # Transform adjacent columns based on blue pixel rows
    left_col = max(0, gray_column_index - gray_column_index)  # Ensure within bounds
    right_col = min(2, gray_column_index - gray_column_index + 2)  # Ensure within bounds

    for row in blue_rows:
        if gray_column_index > 0 :
            output_grid[row,left_col] = 2
        if gray_column_index < input_grid.shape[1]:
            output_grid[row, right_col] = 2


    return output_grid
```