# dc1df850 • 004 • refine_coder

---
```python
"""
1.  **Identify Key Cells:** Find all red (2) and magenta (6) cells in the input grid.
2.  **Check for Both Colors:** If *both* red and magenta cells are present, proceed to step 3. Otherwise, the output is identical to the input (no transformation).
3.  **Bounding Rectangle:** If both colors are present, determine the bounding rectangle. This rectangle is defined by the minimum row, minimum column, maximum row, and maximum column considering the positions of *both* red and magenta cells. In other words:
    *   `min_row = min(min(red_rows), min(magenta_rows))`
    *   `min_col = min(min(red_cols), min(magenta_cols))`
    *   `max_row = max(max(red_rows), max(magenta_rows))`
    *   `max_col = max(max(red_cols), max(magenta_cols))`
4.  **Fill Rectangle:** Within the output grid (initially all zeros), set all cells *inside* the bounding rectangle to blue (1).
5.  **Preserve Markers:** Copy the original red (2) and magenta (6) cells from the input grid to their exact same positions in the output grid. This ensures these boundary markers are preserved on top of the blue fill.
"""

import numpy as np

def find_cells_by_color(grid, color):
    """Finds the positions of cells with the specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Key Cells
    red_cells = find_cells_by_color(input_grid, 2)
    magenta_cells = find_cells_by_color(input_grid, 6)

    # 2. Check for Both Colors
    if len(red_cells) > 0 and len(magenta_cells) > 0:
        # 3. Bounding Rectangle
        min_row = min(red_cells[:, 0].min(), magenta_cells[:, 0].min())
        min_col = min(red_cells[:, 1].min(), magenta_cells[:, 1].min())
        max_row = max(red_cells[:, 0].max(), magenta_cells[:, 0].max())
        max_col = max(red_cells[:, 1].max(), magenta_cells[:, 1].max())

        # 4. Fill Rectangle
        for r in range(min_row, max_row + 1):
            for c in range(min_col, max_col + 1):
                output_grid[r, c] = 1

        # 5. Preserve Markers
        for r, c in red_cells:
            output_grid[r, c] = 2
        for r, c in magenta_cells:
            output_grid[r, c] = 6

        return output_grid.tolist()
    else:
      # no transformation
      return input_grid.tolist()
```
