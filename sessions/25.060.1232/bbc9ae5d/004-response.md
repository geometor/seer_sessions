# bbc9ae5d • 004 • example_1 • investigate_coder

---
```python
"""
Expands a contiguous region of blue (1) pixels in a grid downwards, 
maintaining the original shape's width in each new row.
"""

import numpy as np

def find_blue_region(grid):
    """Finds the bounding box of the blue (1) region."""
    rows, cols = np.where(grid == 1)
    if len(rows) == 0:
        return None  # No blue region found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """Transforms the input grid by expanding the blue region downwards."""
    input_grid = np.array(input_grid)
    blue_region = find_blue_region(input_grid)

    if blue_region is None:
        return input_grid.tolist()  # Return original if no blue region

    min_row, min_col, max_row, max_col = blue_region
    blue_width = max_col - min_col + 1
    blue_height = max_row - min_row + 1
    
    num_white = 0
    for i in range(input_grid.shape[1]):
       if input_grid[0,i] == 0:
           num_white += 1

    # Initialize output grid with original input
    output_grid = input_grid.copy()

    
    #append rows
    rows_to_add = num_white + blue_height -1
    
    for i in range(rows_to_add):
        new_row = np.zeros(input_grid.shape[1],dtype=int)
        output_grid = np.vstack((output_grid,new_row))
    
    #fill in blue region
    row_start = blue_height
    row_end = row_start+rows_to_add
    
    col_start = min_col
    col_end = col_start + blue_width
    
    output_grid[row_start:row_end, col_start:col_end] = 1

    return output_grid.tolist()
```
