# d43fd935 • 022 • refine_coder

---
```python
"""
1. Preserve Green: Copy all green pixels from the input grid to the output grid, maintaining their original positions.
2. Iterative Downward Extension of Blue: For each blue pixel in the input grid:
    * Begin at the cell directly below the blue pixel in the output grid.
    * While the current cell is white and within the grid boundaries:
        * Change the current cell to blue.
        * Move one cell down.
"""

import numpy as np

def find_objects_by_color(grid, color):
    # Find coordinates of all pixels of the specified color.
    objects = []
    rows, cols = np.where(grid == color)
    for r, c in zip(rows, cols):
        objects.append((r, c))
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Preserve Green
    green_objects = find_objects_by_color(input_grid, 3)
    for r, c in green_objects:
        output_grid[r, c] = 3

    # Find blue objects.
    blue_objects = find_objects_by_color(input_grid, 1)

    # Iteratively extend blue pixels downwards.
    for r, c in blue_objects:
        current_row = r + 1
        while current_row < rows and output_grid[current_row, c] == 0:
            output_grid[current_row, c] = 1
            current_row += 1

    return output_grid
```
