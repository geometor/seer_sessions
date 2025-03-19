# cf98881b • 029 • refine_coder

---
```python
"""
1. Identify the key color: Find the color of the pixel in the last row that is different from the first pixel in the last row. If all pixels in the last row are the same, use that color.
2. Remove the outer border: Discard the top and bottom rows and the leftmost and rightmost columns of the input grid.
3. Select columns: Compare the remaining columns (after border removal) to the key color. Keep only the columns from the inner grid that contain the key color.
4. The result is the output.
"""

import numpy as np

def get_key_color(grid):
    # Find the color in the last row that is different from the first pixel's color.
    last_row = grid[-1, :]
    first_color = last_row[0]
    for color in last_row:
        if color != first_color:
            return color
    return first_color  # Return the first color if all are the same

def remove_outer_border(grid):
    # Remove the top and bottom rows and the leftmost and rightmost columns.
    return grid[1:-1, 1:-1]

def select_columns(grid, key_color):
    # Select columns that contain the key color.
    selected_cols = []
    for j in range(grid.shape[1]):
        if key_color in grid[:, j]:
            selected_cols.append(grid[:, j])
    if not selected_cols:
      return np.array([])
    return np.stack(selected_cols, axis=1)


def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Identify the key color
    key_color = get_key_color(input_grid)

    # Remove the outer border
    inner_grid = remove_outer_border(input_grid)
    
    if inner_grid.size == 0:
        return []

    # Select columns based on key color
    output_grid = select_columns(inner_grid, key_color)

    return output_grid.tolist()
```
