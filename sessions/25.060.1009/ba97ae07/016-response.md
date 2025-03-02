# ba97ae07 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation identifies the intersection of a blue vertical line and an orange horizontal line. The pixel at their intersection, originally orange, changes to blue. Everything else stays the same.
"""

import numpy as np

def find_vertical_line(grid, color):
    # Find a vertical line of the specified color.
    rows, cols = grid.shape
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] == color:
                # Check if it's a vertical line
                line_length = 0
                for i in range(r, rows):
                    if grid[i, c] == color:
                        line_length += 1
                    else:
                        break
                if line_length > 1: #consider it is a line if lengh > 1
                    return c, r, line_length #return col, start_row, length
    return None, None, None

def find_horizontal_line(grid, color):
    # Find a horizontal line of the specified color.
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                # Check if it's a horizontal line
                line_length = 0
                for j in range(c, cols):
                    if grid[r, j] == color:
                        line_length += 1
                    else:
                        break

                if line_length > 1:
                    return r, c, line_length
    return None, None, None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the vertical blue line
    blue_col, blue_start_row, blue_length = find_vertical_line(input_grid, 1)

    # Find the horizontal orange line
    orange_row, orange_start_col, orange_length = find_horizontal_line(input_grid, 7)
    
    #check the lines were correctly identified
    if blue_col is not None and orange_row is not None:
        # Change the color of the intersection point to blue if it exists
        if blue_start_row <= orange_row < blue_start_row + blue_length and orange_start_col <= blue_col < orange_start_col + orange_length:
            if output_grid[orange_row, blue_col] == 7:
                output_grid[orange_row, blue_col] = 1

    return output_grid
```
