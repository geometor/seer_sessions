# 662c240a • 006 • refine_coder

---
```python
"""
1.  **Check for Bottom Sub-grid:** If the input grid's bottom three rows consist entirely of color 1, the output grid is the bottom 3x3 sub-grid.
2.  **Check for Top Sub-grid:** If the input grid's top three rows consist entirely of color 1, the output is the top 3x3 sub-grid.
3. **Check for default grids:** If the input grid has uniform 3x3 sections of either colors 5,8,8 or 0, select top 3x3 sub-grid.
4. **Otherwise, empty:** In all other cases, the output is a blank/empty grid.
"""

import numpy as np

def _is_uniform_subgrid(grid, start_row, end_row, color):
    """Checks if a subgrid is uniform with the specified color."""
    subgrid = grid[start_row:end_row, :]
    return np.all(subgrid == color)

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = []

    # Check for Bottom Sub-grid (color 1)
    if _is_uniform_subgrid(input_grid, rows - 3, rows, 1):
        output_grid = input_grid[rows - 3:rows, :].tolist()
    # Check for Top Sub-grid (color 1)
    elif _is_uniform_subgrid(input_grid, 0, 3, 1):
        output_grid = input_grid[0:3, :].tolist()
    # Check for default grids (5,8,8 or 0)
    elif _is_uniform_subgrid(input_grid, 0, 3, input_grid[0,0]) and \
         _is_uniform_subgrid(input_grid, 3, 6, input_grid[0,0]) and \
          _is_uniform_subgrid(input_grid, 6, 9, input_grid[0,0]) and \
         (np.all(input_grid[0:3,:] == [5,8,8]) or np.all(input_grid[0:3] == 0)):
        output_grid = input_grid[0:3, :].tolist()

    return output_grid
```
