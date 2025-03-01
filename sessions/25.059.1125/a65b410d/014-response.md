# a65b410d • 014 • refine_coder

---
```python
"""
Transforms the input grid by expanding a horizontal red line into a pattern of green, red, and blue lines. The output grid has the same dimensions as the input. If no red line is found, output is identical to input.
"""

import numpy as np

def find_red_line(grid):
    # Iterate through rows to find a horizontal line of red pixels
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols - 1):  # Changed to cols - 1
            if grid[r, c] == 2 and grid[r, c+1] == 2:
                length = 0
                for i in range(c,cols):
                    if grid[r,i] == 2:
                        length += 1
                    else:
                        break
                return r, c, length  # row, start_col, length
    return None, None, None

def transform(input_grid):
    # Initialize output grid with the same dimensions and filled with white (0)
    output_grid = np.copy(input_grid)  # Initialize with the input grid
    
    # Find the horizontal red line
    red_row, red_col_start, red_length = find_red_line(input_grid)
    
    if red_row is not None:
        # Create the red line in the output grid
        output_grid[red_row, red_col_start:red_col_start + red_length] = 2

        # Expand Upward (Green lines)
        for i in range(1, min(3, red_row) + 1):  # Up to 3 lines, or until top edge
             green_length = red_length + 1 - i
             green_col_start = red_col_start
             output_grid[red_row - i, green_col_start:min(green_col_start + green_length, output_grid.shape[1])] = 3

        # Expand Downward (Blue lines)
        for i in range(1, min(2, output_grid.shape[0] - red_row -1) + 1):
            blue_length = red_length - i
            blue_col_start = red_col_start
            if blue_length>0:
              output_grid[red_row + i, blue_col_start:min(blue_col_start + blue_length, output_grid.shape[1])] = 1


    return output_grid
```
