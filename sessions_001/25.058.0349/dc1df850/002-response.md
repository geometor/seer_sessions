# dc1df850 • 002 • example_1 • investigate_coder

---
```python
"""
1.  **Locate Key Cells:** Identify the positions of cells with the value '2' (red) and '6' (magenta) within the input grid.
2.  **Preserve Key Cells:** Maintain the color and position of the identified '2' and '6' cells in the output grid.
3. **Determine Top region**: find the min row and min col that has color '2', use this to find the range.
4.  **Fill with Blue (1):** Change the color of the cells in the region bounded by [min_row, min_col] to the value '1' (blue), inclusive. Other cells' values are set to 0.
"""

import numpy as np

def find_cells_by_color(grid, color):
    """Finds the positions of cells with the specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # Locate key cells (color 2 and 6)
    red_cells = find_cells_by_color(input_grid, 2)
    magenta_cells = find_cells_by_color(input_grid, 6)

    # Preserve key cells
    for r, c in red_cells:
        output_grid[r, c] = 2
    for r, c in magenta_cells:
        output_grid[r, c] = 6

    # Determine top region
    if len(red_cells) > 0:
      min_row = min(red_cells[:, 0])
      min_col = min(red_cells[:, 1])

      # Fill with Blue (1)
      for r in range(min_row, input_grid.shape[0]):
          for c in range(min_col, input_grid.shape[1]):
              output_grid[r,c] = 1

    return output_grid.tolist()
```
