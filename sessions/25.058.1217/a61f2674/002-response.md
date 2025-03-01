# a61f2674 • 002 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Gray Lines:** Scan the input grid to locate all contiguous vertical lines composed entirely of gray (5) pixels.
2.  **Transform to Blue:** For each identified gray line, change all of its pixels to blue (1). Maintain the line's original x-coordinate (column) and length.
3.  **Create Red Line:** For each identified gray vertical line, find the bottom of the grid with gray line x, and create a red (2) line segment of two pixels, keeping the same original x-coordinate.
"""

import numpy as np

def find_vertical_gray_lines(grid):
    """Finds the starting positions and lengths of vertical gray lines."""
    gray_lines = []
    rows, cols = grid.shape
    for j in range(cols):
        start_row = -1
        length = 0
        for i in range(rows):
            if grid[i, j] == 5:
                if start_row == -1:
                    start_row = i
                length += 1
            elif start_row != -1:
                gray_lines.append((start_row, j, length))
                start_row = -1
                length = 0
        if start_row != -1:
            gray_lines.append((start_row, j, length))
    return gray_lines

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    output_grid[:] = 0 # initialize to all zeros
    rows, cols = output_grid.shape

    # Find gray lines
    gray_lines = find_vertical_gray_lines(input_grid)

    # Transform gray lines to blue and add red lines
    for start_row, col, length in gray_lines:
        # Transform to blue
        for i in range(start_row, start_row + length):
            output_grid[i, col] = 1

        # Add red line segment at the bottom
        output_grid[rows - 2, col] = 2
        output_grid[rows - 1, col] = 2
    return output_grid
```
