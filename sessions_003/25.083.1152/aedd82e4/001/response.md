```python
"""
Iterate through each column of the input grid, starting from the bottom row and moving upwards.
For each column, find the last (bottom-most) occurrence of the value '2' (red).
If a '2' is found in that column, change its value to '1' (blue) in the output grid.
Iterate through each row of the input grid, start from the right-most column and moving left
For each row, find the last(right-most) occurence of the value '2'(red).
If a '2' is found in that row, change its value to '1'(blue) in the output grid
Copy all other pixel values from the input grid to the output grid unchanged.
ensure that if a '2' has already been changed to a '1' by the column rule, it is not changed again
by the row rule.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through columns from bottom to top
    for j in range(cols):
        last_two_row = -1
        for i in range(rows - 1, -1, -1):
            if output_grid[i, j] == 2:
                last_two_row = i
                break  # Find the *last* occurrence, then stop
        if last_two_row != -1:
            output_grid[last_two_row, j] = 1

    # Iterate through rows from right to left
    for i in range(rows):
        last_two_col = -1
        for j in range(cols-1, -1, -1):
            if output_grid[i,j] == 2:
                last_two_col = j
                break
        if last_two_col != -1:
            output_grid[i, last_two_col] = 1
    return output_grid
```