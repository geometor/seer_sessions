# 46442a0e • 010 • refine_coder

---
```python
"""
The input grid's dimensions are doubled to create an output grid. The output
grid contains an outline of the input object, scaled by a factor of 2, with the
interior filled with the background color (0).
"""

import numpy as np

def is_edge(grid, row, col):
    """
    Checks if a pixel at (row, col) is on the edge of its object in the grid.
    """
    rows, cols = grid.shape
    color = grid[row, col]

    # Check adjacent pixels (up, down, left, right)
    if row > 0 and grid[row - 1, col] != color:
        return True
    if row < rows - 1 and grid[row + 1, col] != color:
        return True
    if col > 0 and grid[row, col - 1] != color:
        return True
    if col < cols - 1 and grid[row, col + 1] != color:
        return True

    return False


def transform(input_grid):
    # Get input grid dimensions
    rows, cols = input_grid.shape

    # Create output grid with doubled dimensions, initialized with zeros (background color)
    output_grid = np.zeros((2 * rows, 2 * cols), dtype=int)

    # Find object and its color
    object_color = 0  # initialization
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] != 0:
          object_color = input_grid[r,c]
          break
      if object_color != 0:
        break
          

    # Iterate through the input grid and create the outline in the output grid
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == object_color:  # Check if the pixel is part of the object
                if is_edge(input_grid, i, j):
                    # Scale the coordinates for the output grid
                    output_grid[2 * i, 2 * j] = object_color
                    output_grid[2 * i + 1, 2 * j] = object_color
                    output_grid[2 * i, 2 * j + 1] = object_color
                    output_grid[2*i + 1, 2*j + 1] = object_color

    return output_grid
```
