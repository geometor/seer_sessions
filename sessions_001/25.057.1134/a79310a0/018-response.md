# a79310a0 • 018 • refine_coder

---
```python
"""
Finds all horizontal lines consisting of exactly three adjacent azure pixels.
For each such line:
    If the line is *not* at the bottom row of the grid, change the color of the pixels in the line from azure to red and move the entire line down by one row.
    If the line *is* at the bottom row of the grid, remove the line.
All other pixels that are not part of a three-azure-pixel horizontal line remain unchanged in their original color and position.
"""

import numpy as np

def find_horizontal_lines(grid, length, color):
    """Finds all horizontal lines of specified length and color."""
    lines = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1] - length + 1):
            if all(grid[i, j+k] == color for k in range(length)):
                lines.append((i, j))
    return lines

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)

    lines = find_horizontal_lines(input_grid, 3, 8)

    for row, col in lines:
        if row + 1 < output_grid.shape[0]:
            # Move down and change to red
            for k in range(3):
                output_grid[row + 1, col + k] = 2  # Set to red
                
            # clear original ONLY if it was azure
            for k in range(3):
              if input_grid[row,col+k] == 8:
                output_grid[row, col + k] = 0 # clear original
        else:
            # Remove the line if at the bottom
            for k in range(3):
                output_grid[row, col + k] = 0

    return output_grid
```
