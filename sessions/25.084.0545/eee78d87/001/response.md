```python
"""
Transforms an input grid into a larger grid with a specific pattern. The input is embedded within the larger grid,
surrounded by a border of alternating 7s and 0s. Non-7 pixels in the embedded input are changed to 9.
The larger grid is also filled with a checkerboard pattern of 7s and 0s.
"""

import numpy as np

def transform(input_grid):
    input_height, input_width = input_grid.shape
    output_height, output_width = 16, 16
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Checker Board Fill
    for r in range(output_height):
      for c in range(output_width):
        if (r + c) % 2 == 0:
          output_grid[r][c] = 0
        else:
          output_grid[r][c] = 7

    # Cross pattern
    center_row = output_height // 2
    center_col = output_width // 2

    cross_h_start = center_row - input_height // 2
    cross_h_end = center_row + (input_height + 1) // 2

    cross_w_start = center_col - input_width // 2
    cross_w_end = center_col + (input_width + 1) // 2

    for r in range(output_height):
      output_grid[r, cross_w_start:cross_w_end] = 0
    
    for c in range(output_width):
      output_grid[cross_h_start:cross_h_end, c] = 0

    # Embed Input and Replace
    row_offset = (output_height - input_height) // 2
    col_offset = (output_width - input_width) // 2

    for r in range(input_height):
      for c in range(input_width):
        if (row_offset + r >= cross_h_start and row_offset + r < cross_h_end) or (col_offset + c >= cross_w_start and col_offset + c < cross_w_end):
          if input_grid[r, c] != 7:
            output_grid[row_offset + r, col_offset + c] = 9
        else:
          if input_grid[r, c] != 7:
            output_grid[row_offset + r, col_offset + c] = 9
          else:
            output_grid[row_offset + r, col_offset + c] = input_grid[r, c]

    return output_grid
```