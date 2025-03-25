```python
"""
1.  **Locate Gray Column:** Find the index of the column containing gray (5) pixels within the input grid. There should be only one such column.
2.  **Identify Blue Neighbors:** For each row, check if there's a blue (1) pixel immediately to the left or right of the gray column.
3.  **Determine Output Column Count:** If a blue pixel exists to the left, increment column count by one, and if to the right increment column count by one.
4.  **Construct Output Grid:**
    *   Create an output grid with dimensions based on number of rows in input and columns based on blue neighbor count.
    *   Iterate through each row of the input grid.
        *   If a blue pixel was found to the left of the gray column in that row, place a red (2) pixel in the first column of the output grid at the same row.
        *   If a blue pixel was found to the right of the gray column in that row, place a red (2) pixel in the second column (if exists) of the output grid at the same row.
        *    All other pixels in the output grid should be white (0).
5.  **Return the output grid.**
"""

import numpy as np

def find_gray_column(grid):
    """Finds the index of the column containing gray (5)."""
    for j in range(grid.shape[1]):
        if 5 in grid[:, j]:
            return j
    return -1

def count_blue_neighbors(grid, gray_column_index):
    """Counts the number of columns needed based on blue neighbors (left and/or right)."""
    left_count = 0
    right_count = 0

    for i in range(grid.shape[0]):
        if gray_column_index > 0 and grid[i, gray_column_index - 1] == 1:
            left_count = 1
            break #we are only counting if any blues exist, not how many
    for i in range(grid.shape[0]):
        if gray_column_index < grid.shape[1] - 1 and grid[i, gray_column_index + 1] == 1:
            right_count = 1
            break

    return left_count + right_count


def transform(input_grid):
    # Find gray column
    gray_column_index = find_gray_column(input_grid)

    if gray_column_index == -1:
        return np.zeros((input_grid.shape[0], 0), dtype=int)

    # Determine output width
    output_width = count_blue_neighbors(input_grid, gray_column_index)
    #print(f"{output_width=}")

    # Initialize output grid
    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)


    # Fill output grid
    col_index = 0
    for row_index in range(input_grid.shape[0]):
      if gray_column_index > 0 and input_grid[row_index, gray_column_index - 1] == 1:
        output_grid[row_index,col_index] = 2
    
    if output_width == 2: #we know there must be a right column, so add 1 to the col_index
      col_index = 1

    for row_index in range(input_grid.shape[0]):
      if gray_column_index < (input_grid.shape[1] - 1) and input_grid[row_index, gray_column_index + 1] == 1:
        output_grid[row_index,col_index] = 2

    return output_grid
```