# 6430c8c4 • 024 • refine_coder

---
```python
"""
1.  **Identify the Orange Shape:** Find all pixels in the input grid that are colored orange (7).
2.  **Determine Bounding Box:** Calculate the bounding box (minimum and maximum row and column) of the connected orange shape.
3.  **Create Output Grid:** Create a new grid filled with black (0) with dimensions equal to the bounding box of the orange shape.
4.  **Replace Color:** Within the output grid, replace black with green (3) at the relative positions where orange pixels were found within the input's bounding box. i.e., If an orange pixel was found at `input_grid[min_row + i][min_col + j]`, set `output_grid[i][j]` to green.
"""

import numpy as np

def get_bounding_box(grid, color):
    orange_pixels = np.argwhere(grid == color)
    if orange_pixels.size > 0:
        min_row, min_col = np.min(orange_pixels, axis=0)
        max_row, max_col = np.max(orange_pixels, axis=0)
        return (min_row, min_col, max_row + 1, max_col + 1)  # +1 for inclusive
    else:
        return (0, 0, 0, 0)

def transform(input_grid):
    # Find all pixels in the input grid that are colored orange (7).
    input_grid = np.array(input_grid)
    
    # Determine Bounding Box
    min_row, min_col, max_row, max_col = get_bounding_box(input_grid, 7)

    # Create Output Grid: dimensions equal to the bounding box of orange shape
    output_grid_height = max_row - min_row
    output_grid_width = max_col - min_col
    output_grid = np.zeros((output_grid_height, output_grid_width), dtype=int)


    # Replace Color
    for i in range(min_row, max_row):
        for j in range(min_col, max_col):
            if input_grid[i, j] == 7:
                output_grid[i - min_row, j - min_col] = 3

    return output_grid
```
