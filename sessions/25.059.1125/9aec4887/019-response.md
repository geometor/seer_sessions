# 9aec4887 • 019 • refine_coder

---
```python
"""
1.  **Identify Boundary Markers:**  The input grid contains an azure (color 8) shape.  It also has horizontal orange (7) and blue (1) lines at the top and bottom, and yellow (4) and magenta (6) pixels marking columns.
2.  **Define Region of Interest:**  The output grid is a rectangular subgrid of the input. This subgrid starts at the row of the orange line and extends to the row of the blue line. The left column is marked by the yellow pixel and the right by the magenta pixel. This region includes the azure shape, even if it extends beyond the yellow/magenta column markers or the orange/blue row markers.
3. **Remove empty columns:** Remove any columns from the extracted subgrid which contains all zeros.
4.  **Output:** The final output is the subgrid with all the non-zero columns.
"""

import numpy as np

def find_object(grid, color):
    coords = np.argwhere(grid == color)
    if coords.size > 0:
         return coords
    return None

def get_bounding_box(grid):

    orange_line = find_object(grid, 7)
    blue_line =  find_object(grid, 1)
    yellow_line = find_object(grid, 4)
    magenta_line = find_object(grid, 6)
    azure_shape = find_object(grid,8)

    min_row = orange_line[0][0] if orange_line is not None else 0
    max_row = blue_line[0][0] if blue_line is not None else grid.shape[0] -1
    min_col = yellow_line[0][1] if yellow_line is not None else 0
    max_col = magenta_line[0][1] if magenta_line is not None else grid.shape[1] - 1

    if azure_shape is not None:
        min_azure_row = np.min(azure_shape[:, 0])
        max_azure_row = np.max(azure_shape[:, 0])
        min_azure_col = np.min(azure_shape[:, 1])
        max_azure_col = np.max(azure_shape[:, 1])

        min_row = min(min_row, min_azure_row)
        max_row = max(max_row, max_azure_row)
        min_col = min(min_col, min_azure_col)
        max_col = max(max_col, max_azure_col)


    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # Get the bounding box
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)

    # Extract the subgrid
    subgrid = input_grid[min_row:max_row+1, min_col:max_col+1]

    #Remove 0 columns
    
    # Find indices of columns that contain non-zero values.
    non_zero_cols = np.any(subgrid != 0, axis=0)
    # Use boolean indexing to select only columns with non-zero values.
    output_grid = subgrid[:, non_zero_cols]
    
    return output_grid
```
