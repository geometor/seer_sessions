# a65b410d • 012 • refine_coder

---
```python
"""
Transforms the input grid by expanding a horizontal red line into a pattern of green, red, and blue lines. The output grid has the same dimensions as the input.
"""

import numpy as np

def find_red_line(grid):
    # Iterate through rows to find a horizontal line of red pixels
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols - 2):
            if grid[r, c] == 2 and grid[r, c+1] == 2 and grid[r, c+2] == 2:
                return r, c, 3  # row, start_col, length
    return None, None, None

def transform(input_grid):
    # Initialize output grid with the same dimensions and filled with white (0)
    output_grid = np.zeros_like(input_grid)
    
    # Find the horizontal red line
    red_row, red_col_start, red_length = find_red_line(input_grid)
    
    if red_row is not None:
        # Create the red line in the output grid
        output_grid[red_row, red_col_start:red_col_start + red_length] = 2

        # Expand Upward (Green lines)
        for i in range(1, 4):
            green_length = red_length + i -1
            green_col_start = red_col_start - i + 1
            if green_col_start < 0:
                green_length = green_length + green_col_start
                green_col_start = 0
            output_grid[red_row - i, green_col_start:min(green_col_start + green_length, output_grid.shape[1])] = 3

        # Expand Downward (Blue lines)
        
        blue_length = red_length - 1 if red_length > 2 else 2

        blue_col_start = red_col_start
        if red_row + 1 < output_grid.shape[0]:
          output_grid[red_row + 1, blue_col_start:min(blue_col_start + blue_length, output_grid.shape[1])] = 1
        if red_row + 2 < output_grid.shape[0]:
          output_grid[red_row + 2, blue_col_start:min(blue_col_start + 1, output_grid.shape[1])] = 1


    return output_grid
```
