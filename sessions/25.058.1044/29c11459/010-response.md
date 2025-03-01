# 29c11459 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Locate:** Find the green pixel (value 3) and the orange pixel (value 7) in the fourth row of the input grid.
2.  **Expand Green:** Replicate the green pixel horizontally to the right, until the middle of between green and orange pixel.
3.  **Expand Orange:** Replicate the orange pixel horizontally to the left, until the middle of between green and orange pixel.
4.  **Insert Grey**: Create the grey pixel (value 5) in between left and right expansion.
5. **Preserve others**: Other pixels in the grid keep its value.
"""

import numpy as np

def find_pixel(grid, value):
    """Finds the coordinates of a pixel with a specific value."""
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == value:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find the green (3) and orange (7) pixels
    green_pos = find_pixel(input_grid, 3)
    orange_pos = find_pixel(input_grid, 7)
    
    if green_pos is None or orange_pos is None:
      return output_grid

    # Determine the middle column index
    middle_col = (green_pos[1] + orange_pos[1]) // 2

    # Expand green to the right
    for j in range(green_pos[1], middle_col):
        output_grid[green_pos[0]][j] = 3

    # Expand orange to the left
    for j in range(middle_col + 1, orange_pos[1] + 1):
        output_grid[orange_pos[0]][j] = 7
    
    # Insert grey(5)
    output_grid[green_pos[0]][middle_col] = 5


    return output_grid
```
