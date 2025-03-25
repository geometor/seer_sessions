```python
"""
1.  **Identify Red Pixel Pattern:** Examine the bottom row of the input grid. Note the column indices where red pixels (value 2) are located. These columns define the vertical pattern.

2.  **Replicate Vertically:** Create the output grid. For *every* row in the output grid, place red pixels (value 2) in the columns identified in step 1.

3.  **Place Gray Pixels:** For each gray pixel (value 5) in the *input* grid, find its row and column. In the *output* grid, place the gray pixel at the same row. Now, consider the new column for each gray pixel.
    * if the gray pixel in the output grid has any red pixels that are to its left, then its column position is shifted one unit to the left.
    * otherwise, the gray pixel maintains the same column as the input.
"""

import numpy as np

def find_pattern_row(grid):
    # Find the row index with red pixels (value 2).
    for i, row in enumerate(grid):
        if 2 in row:
            return i
    return None  #should not reach here by design

def get_red_columns(grid, pattern_row_index):
     #Get the column indices where red pixels are present in the pattern row.
    red_columns = []
    for j, pixel in enumerate(grid[pattern_row_index]):
        if pixel == 2:
           red_columns.append(j)
    return red_columns

def find_gray_pixels(grid):
    """Finds the coordinates of gray pixels (value 5) in the grid."""
    gray_pixels = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 5:
                gray_pixels.append((r_idx, c_idx))
    return gray_pixels
    
def transform(input_grid):
    """Transforms the input grid according to the observed pattern."""

    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    
    # 1. Identify the Pattern Row (row with red pixels)
    pattern_row_index = find_pattern_row(input_grid)

    # 2. Get Red Columns from Pattern Row
    red_columns = get_red_columns(input_grid, pattern_row_index)
    
    # 3. Replicate Red Pattern Vertically
    for r_idx in range(output_grid.shape[0]):
        for c_idx in red_columns:
            output_grid[r_idx, c_idx] = 2

    # 4. Find and place gray pixels
    gray_pixels = find_gray_pixels(input_grid)
    
    for gray_r, gray_c in gray_pixels:
        new_gray_c = gray_c
        for c in red_columns:
          if gray_c > c:
            new_gray_c = gray_c -1
            break # only shift once
        output_grid[gray_r, new_gray_c] = 5
            
    return output_grid
```