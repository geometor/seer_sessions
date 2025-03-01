# 56dc2b01 • 020 • refine_coder

---
```python
"""
1.  **Identify and Preserve Red Line:** Find the horizontal line of red (2) pixels in the input grid. Copy this line to the output grid in the same row position.

2.  **Identify, Modify, and Shift Green Object:** Find the largest contiguous block of green (3) pixels. If this block exists, copy the bottom *two* rows of this green object to the output, *unless* there are fewer than two rows, then copy all available rows. Place the copied green rows to the row immediately below the red line in the output grid.

3.  **Add Azure Line:** Add a horizontal line of azure (8) pixels to the output grid.  This line should be positioned three rows below the bottom of the modified green object, or three rows below the red line if no green object. The length of the azure line should always match width of grid.

4. **Clear other:** set value of other cells to white/0.
"""

import numpy as np

def find_horizontal_line(grid, color):
    """Finds the row index of a horizontal line of the given color."""
    for row_index in range(grid.shape[0]):
        line_cols = np.where(grid[row_index,:] == color)[0]
        if line_cols.size > 0 and np.all(grid[row_index, line_cols[0]:line_cols[-1]+1] == color):
            return row_index
    return None

def find_object(grid, color):
    """Finds the bounding box of the largest contiguous block of the given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    output_grid[:] = 0

    # 1. Identify and Preserve Red Line
    red_line_row = find_horizontal_line(input_grid, 2)
    if red_line_row is not None:
        red_cols = np.where(input_grid[red_line_row, :] == 2)[0]
        output_grid[red_line_row, red_cols[0]:red_cols[-1]+1] = 2

    # 2. Identify, Modify, and Shift Green Object
    green_object = find_object(input_grid, 3)
    new_green_start_row = red_line_row + 1 if red_line_row is not None else None

    if green_object is not None and new_green_start_row is not None:
        (green_min_row, green_min_col), (green_max_row, green_max_col) = green_object
        rows_to_copy = min(2, green_max_row - green_min_row + 1)
        green_width = green_max_col - green_min_col + 1

        if new_green_start_row + rows_to_copy <= output_grid.shape[0]:
            output_grid[new_green_start_row:new_green_start_row+rows_to_copy, green_min_col:green_min_col+green_width] = input_grid[green_max_row-rows_to_copy+1:green_max_row+1, green_min_col:green_min_col+green_width]


    # 3. Add Azure Line
    if red_line_row is not None:
        if green_object is not None:
            azure_row = new_green_start_row + rows_to_copy + 2
        else:
            azure_row = red_line_row + 3

        if azure_row < output_grid.shape[0]:
                output_grid[azure_row,:] = 8

    return output_grid
```
