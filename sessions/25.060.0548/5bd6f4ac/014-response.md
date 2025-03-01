# 5bd6f4ac • 014 • refine_coder

---
```python
"""
1. **Identify Subgrids:** Scan the input grid to identify rectangular subgrids. A subgrid is defined as a contiguous block of pixels of the same color, fully surrounded by pixels of a *different* color, or the edge of the grid. The different surrounding color could vary.
2. **Extract Subgrid:** Extract the identified subgrid.
3. **Output:** The extracted subgrid is the output grid.
"""

import numpy as np

def find_subgrid(input_grid):
    """Helper function to locate a subgrid within the input grid."""
    rows, cols = input_grid.shape
    max_rows = 0
    max_cols = 0
    best_r = -1
    best_c = -1
    best_color = -1

    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color == 0:
                continue

            # Check for different color boundary
            is_bounded = True
            subgrid_rows = 0
            subgrid_cols = 0

            # Find height
            for rr in range(r, rows):
              if input_grid[rr,c] != color:
                break;
              subgrid_rows += 1

            # Find width
            for cc in range(c, cols):
              if input_grid[r, cc] != color:
                break
              subgrid_cols += 1

            # Check the borders
            # top
            if (r > 0):
              for j in range(c, c + subgrid_cols):
                if (j < cols):
                  if (input_grid[r-1,j] == color):
                    is_bounded = False
                    break

            # bottom
            if (is_bounded and r + subgrid_rows < rows):
              for j in range(c, c + subgrid_cols):
                if (j < cols):
                  if (input_grid[r+subgrid_rows,j] == color):
                    is_bounded = False
                    break

            # left
            if (is_bounded and c > 0):
               for i in range(r, r + subgrid_rows):
                  if (i < rows):
                    if (input_grid[i, c-1] == color):
                      is_bounded = False
                      break

            # right
            if (is_bounded and c + subgrid_cols < cols):
              for i in range(r, r + subgrid_rows):
                if (i < rows):
                  if (input_grid[i, c + subgrid_cols] == color):
                    is_bounded = False
                    break

            if (is_bounded):
              if (subgrid_rows * subgrid_cols > max_rows * max_cols):
                max_rows = subgrid_rows
                max_cols = subgrid_cols
                best_r = r
                best_c = c
                best_color = color

    if best_color != -1:
        return input_grid[best_r:best_r + max_rows, best_c:best_c + max_cols], best_r, best_c, max_rows, max_cols
    else:
        return None, -1, -1, -1, -1


def transform(input_grid):
    # Locate the subgrid.
    subgrid, r_start, c_start, num_rows, num_cols = find_subgrid(input_grid)

    # Check if a subgrid was found
    if subgrid is not None:
      output_grid = subgrid
    else:
      output_grid = np.zeros((3, 3), dtype=int) # a default grid

    return output_grid
```
