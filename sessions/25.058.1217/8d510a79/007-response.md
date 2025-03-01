# 8d510a79 • 007 • refine_coder

---
```python
"""
1.  **Find the Separator:** Locate the row index of the horizontal line composed entirely of gray pixels (value 5). This row divides the grid into an upper and lower section. If no separator is found, the input grid is returned unchanged.

2.  **Iterate and Identify:** Examine each cell of the input grid.
    *   If a cell is above the separator and is blue (1) or red (2), extend that pixel downwards.
        The pixel's color value replaces the values of the blank (0) cells below until it reaches a non-zero cell above the separator.

    *   If a cell is *below* the separator and contains a blue (1) or red (2) pixel, extend that pixel upwards.
        The pixel value replaces the values of the blank (0) cells above it until it reaches a non-zero cell below the separator.

3.  **Output:** Return the modified grid.
"""

import numpy as np

def find_separator_row(grid):
    # Iterate through rows to find the row consisting entirely of gray (5) pixels
    for i, row in enumerate(grid):
        if np.all(row == 5):
            return i
    return -1  # Separator not found

def extend_pixel(grid, row, col, direction, separator_row):
    # Extend the pixel vertically based on direction and separator
    rows, cols = grid.shape
    color = grid[row, col]

    if direction == "down":
      next_row = row + 1
      while next_row < rows and next_row < separator_row:
        if grid[next_row, col] == 0:
          grid[next_row,col] = color
          next_row += 1
        else:
          break #stop at non-zero

    elif direction == "up":
        next_row = row - 1
        while next_row >= 0 and next_row > separator_row:
            if grid[next_row, col] == 0:
                grid[next_row, col] = color
                next_row -= 1
            else:
              break #stop at non-zero

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the separator row
    separator_row = find_separator_row(output_grid)
    if separator_row == -1:
        return output_grid  # No separator, return input as is

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # Process blue (1) and red (2) pixels
            if output_grid[r, c] == 1 or output_grid[r, c] == 2:
                if r < separator_row:
                    # Extend downwards
                    extend_pixel(output_grid, r, c, "down", separator_row)
                elif r > separator_row:
                    # Extend upwards
                    extend_pixel(output_grid, r, c, "up", separator_row)

    return output_grid
```

