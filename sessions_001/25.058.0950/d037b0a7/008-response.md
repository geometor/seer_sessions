# d037b0a7 • 008 • example_1 • investigate_coder

---
```python
"""
1. Identify the magenta-colored cell (value 6) in the top-right corner (0, 2).
2. Propagate the value '6' from the top-right cell to the cells directly below it (1,2) and (2,2).
3. Identify the yellow colored cell (value 4) in the center (1,1)
4. Propagate the value '4' to the cell directly below it (2,1)
"""

import numpy as np

def get_cell_by_value(grid, value):
    # Find the coordinates of a cell with a specific value.
    coords = np.where(grid == value)
    if len(coords[0]) > 0:
       return (coords[0][0], coords[1][0])
    return None
    

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the cell with value 6 (magenta).
    magenta_cell = get_cell_by_value(input_grid, 6)
    if magenta_cell:

      # Propagate '6' downwards.
      for row in range(magenta_cell[0] + 1, rows):
          output_grid[row, magenta_cell[1]] = 6

    #Find cell with value 4
    yellow_cell = get_cell_by_value(input_grid, 4)
    if yellow_cell:
       #propagate 4 down
       for row in range(yellow_cell[0] + 1, rows):
          output_grid[row, yellow_cell[1]] = 4

    return output_grid
```
