# d687bc17 • 008 • refine_coder

---
```python
"""
Identifies a boundary formed by blue (1) pixels.  Within this boundary, non-blue and non-white pixels "drop" downwards, filling empty (white, 0) cells until they encounter a blue pixel, another non-blue/non-white pixel, or the grid edge.
"""

import numpy as np

def find_boundary_bounds(grid):
    # Find the min and max column indices of blue pixels.
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:  # No blue pixels, no boundary
        return None
    min_col, max_col = np.min(cols), np.max(cols)
    min_row, max_row = np.min(rows), np.max(rows) # added this
    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Initialize output grid.
    output_grid = np.copy(input_grid)
    bounds = find_boundary_bounds(input_grid)
     
    if bounds is None:
        return output_grid

    min_row, max_row, min_col, max_col = bounds

    # Iterate through columns within the boundary.
    for c in range(min_col, max_col + 1):
        # "Drop fill" within the column.
        for r in range(min_row, max_row + 1):
            if output_grid[r, c] != 1 and output_grid[r,c] != 0:  # Non-blue and non-white pixel
                current_color = output_grid[r, c]
                drop_row = r + 1
                while drop_row <= max_row :
                    if output_grid[drop_row, c] == 0:  # Empty cell
                        output_grid[drop_row, c] = current_color
                        output_grid[drop_row-1, c] = 0 if output_grid[drop_row-1,c] == current_color and drop_row -1 != r else output_grid[drop_row-1,c] # added to remove the original
                        drop_row += 1
                    elif output_grid[drop_row,c] == 1:
                        break
                    elif output_grid[drop_row,c] != 0:
                        break

                    else:
                       break

    return output_grid
```
