# 508bd3b6 • 008 • refine_coder

---
```python
"""
A diagonal line of green (3) pixels is drawn, starting at the fifth column (index 4) of the grid. The line extends downwards and to the right, increasing the column index by one for each row. The green line stops one row *above* the row where either an azure (8) pixel or a red (2) pixel is encountered in the same column. The precedence is given to the object that has the smallest row number. If neither a red nor an azure pixel is found in the columns traversed by the diagonal, the green line extends to the bottom row of the grid. The red and azure pixels themselves are not modified.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def get_stopping_row(input_grid, start_col):
    """
    Calculates the row index where the green line should stop.
    Considers both red (2) and azure (8) objects, and grid boundaries
    Returns the row index *above* the first obstacle encountered.
    """
    rows, cols = input_grid.shape
    red_pixels = find_object_by_color(input_grid, 2)
    azure_pixels = find_object_by_color(input_grid, 8)

    stopping_row = rows  # Default: go to the bottom

    # Iterate through possible diagonal positions
    for row in range(rows):
        col = start_col + row
        if col >= cols:
            break  # Stop if the diagonal goes out of bounds

        # Check for red pixels
        for red_row, red_col in red_pixels:
            if red_col == col and red_row > row :
                stopping_row = min(stopping_row, red_row -1)


        # Check for azure pixels
        for azure_row, azure_col in azure_pixels:
            if azure_col == col and azure_row > row:
                stopping_row = min(stopping_row, azure_row - 1)

    return stopping_row

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Determine the starting column (always the fifth column - index 4).
    start_col = 4

    # Check if start_col is within bounds
    if start_col >= cols:
        return output_grid # Return original if out of bounds

    # calculate stop row
    stop_row = get_stopping_row(input_grid, start_col)

    # Draw the diagonal green line.
    for row in range(rows):
        col = start_col + row
        if col < cols and row <= stop_row:
            output_grid[row, col] = 3
        else:
          break

    return output_grid
```
