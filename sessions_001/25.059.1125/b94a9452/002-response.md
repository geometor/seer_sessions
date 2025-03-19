# b94a9452 • 002 • example_3 • investigate_coder

---
```python
"""
Finds a shape in the input grid, identifies its inner and outer colors, inverts those colors, and creates a new, smaller grid representing the inverted shape, focusing only on the "core" of the shape and one layer of surrounding pixels.
"""

import numpy as np

def find_shape(grid):
    """Finds the bounding box of the non-zero region in the grid."""
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty shapes (all zeros)
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def get_inner_outer_colors(grid, min_row, max_row, min_col, max_col):
    """Determines the inner and outer colors of the shape."""
    # Outer color is the color at the boundary of the bounding box.
    outer_color = grid[min_row, min_col]
    # Find a different color within the bounding box for inner color
    for i in range(min_row, max_row + 1):
        for j in range(min_col, max_col + 1):
            if grid[i,j] != outer_color:
                inner_color = grid[i,j]
                return inner_color, outer_color
    return None, outer_color # if no distinct inner color found, inner is None

def expand_bbox(min_row, max_row, min_col, max_col, grid_rows, grid_cols):
    """Enlarges the bounding box by one pixel on all sides, respecting grid boundaries."""
    min_row = max(0, min_row - 1)
    max_row = min(grid_rows - 1, max_row + 1)
    min_col = max(0, min_col - 1)
    max_col = min(grid_cols - 1, max_col + 1)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid according to the described logic."""
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # 1. Identify the Shape (Bounding Box)
    min_row, max_row, min_col, max_col = find_shape(grid)
    if min_row is None:  # No shape found
        return []
    
    # 2. Extract and expand relevant section
    min_row, max_row, min_col, max_col = expand_bbox(min_row, max_row, min_col, max_col, rows, cols)
    
    # 3. Determine Inner and Outer Colors
    inner_color, outer_color = get_inner_outer_colors(grid, min_row, max_row, min_col, max_col)

    # 4. Create Output Grid and Invert Colors in extracted section
    output_grid = np.full((max_row - min_row + 1, max_col - min_col + 1), outer_color if inner_color is not None else outer_color )

    for i in range(min_row, max_row+1):
        for j in range(min_col, max_col + 1):
            if grid[i,j] == inner_color:
                output_grid[i-min_row, j-min_col] = outer_color
            elif grid[i,j] == outer_color:
                if inner_color is not None:
                    output_grid[i-min_row, j-min_col] = inner_color


    return output_grid.tolist()
```
