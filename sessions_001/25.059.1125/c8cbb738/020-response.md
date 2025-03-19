# c8cbb738 • 020 • refine_coder

---
```python
"""
Identifies the bounding box defined by blue pixels in the input grid and copies the corresponding subgrid to a new grid, replacing yellow pixels with black.
"""

import numpy as np

def get_blue_pixel_extents(grid):
    """
    Finds the minimum and maximum row and column indices of blue (1) pixels.
    Optimized version.
    """
    rows = np.any(grid == 1, axis=1)
    cols = np.any(grid == 1, axis=0)
    if not np.any(rows) or not np.any(cols):
        return None, None, None, None  # No blue pixels

    min_row, max_row = np.where(rows)[0][[0, -1]]
    min_col, max_col = np.where(cols)[0][[0, -1]]

    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Convert input_grid to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Target Pixels and Determine Bounding Box (optimized)
    min_row, max_row, min_col, max_col = get_blue_pixel_extents(input_grid)

    if min_row is None:  # Handle cases with no blue pixels
        return [[]]

    # 2. Create Output Grid based on the *exact* bounding box dimensions
    output_height = max_row - min_row + 1
    output_width = max_col - min_col + 1
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 3. Copy Subgrid and replace yellow with black
    for i in range(output_height):
        for j in range(output_width):
            original_row = min_row + i
            original_col = min_col + j
            
            #check that the row and col are within the input_grid bounds
            if 0 <= original_row < input_grid.shape[0] and 0 <= original_col < input_grid.shape[1]:
                pixel_value = input_grid[original_row, original_col]
                # Replace yellow (4) with black (0)
                if pixel_value == 4:
                    output_grid[i, j] = 0
                else:
                    output_grid[i, j] = pixel_value


    return output_grid.tolist()
```
