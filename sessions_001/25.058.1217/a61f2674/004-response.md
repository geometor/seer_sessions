# a61f2674 • 004 • example_1 • investigate_coder

---
```python
"""
1. Identify the continuous vertical column of gray pixels in the input grid.
2. Change the color of all pixels within this column from gray to blue.
3. Locate all white cells within the last three rows of the last column.
4. Change the color of these white cells to red.
5. Keep all the other cells unchanged.
"""

import numpy as np

def find_vertical_line(grid, color):
    rows, cols = grid.shape
    for j in range(cols):
        for i in range(rows):
            if grid[i, j] == color:
                # Check if it's a continuous line
                line_length = 0
                for k in range(i, rows):
                    if grid[k, j] == color:
                        line_length += 1
                    else:
                        break
                if line_length > 1:  # Assuming a line has at least 2 pixels
                    return j, i, line_length
    return None

def transform(input_grid):
    # Initialize output grid with a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the vertical gray line
    line_info = find_vertical_line(input_grid, 5)
    if line_info:
        col_index, start_row, length = line_info
        # Change the color of the line to blue
        for i in range(start_row, start_row + length):
            output_grid[i, col_index] = 1

    # Change white cells in the last three rows of the last column to red
    for i in range(rows - 3, rows):
        if output_grid[i, cols - 1] == 0:
            output_grid[i, cols - 1] = 2

    return output_grid
```
