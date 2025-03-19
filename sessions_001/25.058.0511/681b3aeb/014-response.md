# 681b3aeb • 014 • example_3 • investigate_coder

---
```python
"""
Transforms the input grid by extracting the green and blue regions and placing them in a smaller 3x3 output grid.
The blue region is placed in the top row, and the green region is placed in the bottom two rows.
"""

import numpy as np

def get_bounding_box(grid, color):
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Handle the case where the color is not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Initialize output_grid as a 3x3 array filled with zeros (white)
    output_grid = np.zeros((3, 3), dtype=int)

    # Get bounding box for green (3) region
    green_bbox = get_bounding_box(input_grid, 3)
    if green_bbox:
        min_row_g, max_row_g, min_col_g, max_col_g = green_bbox
        # Place green region in the output grid, at the bottom, centered
        for r in range(min_row_g, max_row_g+1):
          for c in range(min_col_g, max_col_g + 1):
            if input_grid[r,c] == 3:
              output_grid[2 - (max_row_g - r) , 1 - (max_col_g - c) ] = 3
    
    # Get bounding box for blue (1) region
    blue_bbox = get_bounding_box(input_grid, 1)
    if blue_bbox:
        min_row_b, max_row_b, min_col_b, max_col_b = blue_bbox
        # Place blue region above, horizontally centered
        for r in range(min_row_b, max_row_b + 1):
          for c in range(min_col_b,max_col_b + 1):
            if input_grid[r,c] == 1:
                output_grid[0, c - min_col_b] = 1

    return output_grid
```
