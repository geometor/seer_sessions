# a79310a0 • 016 • refine_coder

---
```python
"""
Finds all horizontal lines consisting of exactly three adjacent azure pixels.
For each such line:
    Change the color of the pixels in the line from azure to red.
    Move the entire line down by one row.
Preserve all other pixels. Pixels that are not part of a three-azure-pixel horizontal line remain unchanged in color and position.
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
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find all horizontal lines of three azure pixels
    lines = find_horizontal_lines(input_grid, 3, 8)

    # For each line found:
    for row, col in lines:
        # change color to red and move down by one row, *if* within bounds
        if row + 1 < output_grid.shape[0]:
          for k in range(3):
            # Clear original line
            output_grid[row,col+k] = input_grid[row,col+k] if input_grid[row,col+k] != 8 else 0 # preserve non azure
            output_grid[row + 1, col + k] = 2

    return output_grid
```
