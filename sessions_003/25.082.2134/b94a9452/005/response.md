```python
"""
1.  **Isolate Non-Zero Region:** Determine the smallest rectangular sub-grid within the input grid that encompasses all non-zero pixels. This is the "isolated region."

2.  **Color Transformation:** Within the isolated region, apply the following color transformation rule:
    *   If the color is 4, change it to 2.
    *   If the color is 3, change it to 1.
    *   If the color is 6, change it to 4.
    *   All the other colors inside the isolated region remain unchanged.

3.  **Rotate:** Rotate the transformed isolated region 90 degrees clockwise. This rotated region is the final output.
"""

import numpy as np

def _find_non_zero_region(grid):
    rows = np.any(grid != 0, axis=1)
    cols = np.any(grid != 0, axis=0)
    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]
    return min_row, max_row, min_col, max_col

def _transform_colors(grid):
    # Create a copy to avoid modifying the original grid
    transformed_grid = grid.copy()
    # Apply color transformation rules
    transformed_grid[grid == 4] = 2
    transformed_grid[grid == 3] = 1
    transformed_grid[grid == 6] = 4
    return transformed_grid

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # 1. Isolate Non-Zero Region
    min_row, max_row, min_col, max_col = _find_non_zero_region(input_grid)
    isolated_region = input_grid[min_row:max_row+1, min_col:max_col+1]

    # 2. Color Transformation
    transformed_region = _transform_colors(isolated_region)

    # 3. Rotate
    rotated_region = np.rot90(transformed_region, k=-1)

    return rotated_region.tolist()
```
