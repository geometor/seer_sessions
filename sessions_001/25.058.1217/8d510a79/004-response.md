# 8d510a79 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify the Separator:** Locate the horizontal line of gray (5) pixels.
2.  **Process Above Separator:** For each blue (1) or red (2) pixel *above* the gray line, replicate that pixel's color in the cell immediately *below* it, within the same column. If a cell in between is already occupied skip to the next unoccupied.
3.  **Process Below Separator:** For each blue (1) or red (2) pixel *below* the gray line, replicate that pixel's color in the cell immediately *above* it, within the same column.If a cell in between is already occupied skip to the next unoccupied.
4. White(0) pixels remain unchanged.
5. Gray(5) horizontal line remains unchanged.
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
          break
        else:
          next_row +=1

    elif direction == "up":
        next_row = row -1
        while next_row >= 0 and next_row > separator_row:
            if grid[next_row, col] == 0:
                grid[next_row, col] = color
                break
            else:
              next_row -= 1


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
