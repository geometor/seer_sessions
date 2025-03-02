# bbc9ae5d • 006 • refine_coder

---
```python
"""
Expands a contiguous region of blue (1) pixels in a grid downwards, 
maintaining the original shape's width. The expansion's height is determined by
the number of empty rows below and above the original blue region and the input grid height.
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

def count_empty_rows(grid, blue_region):
    """Counts empty rows above and below the blue region."""
    if blue_region is None:
        return 0, 0

    min_row, _, max_row, _ = blue_region
    empty_rows_above = min_row
    empty_rows_below = grid.shape[0] - max_row - 1
    return empty_rows_above, empty_rows_below

def transform(input_grid):
    """Transforms the input grid by expanding the blue region downwards."""
    input_grid = np.array(input_grid)
    blue_region = find_blue_region(input_grid)

    if blue_region is None:
        return input_grid.tolist()  # Return original if no blue region

    min_row, min_col, max_row, max_col = blue_region
    blue_width = max_col - min_col + 1
    blue_height = max_row - min_row + 1
    
    empty_rows_above, empty_rows_below = count_empty_rows(input_grid, blue_region)
    
    rows_to_add = empty_rows_above + empty_rows_below

    # Initialize output grid with original input
    output_grid = input_grid.copy()

    
    #append rows
    
    for i in range(rows_to_add):
        new_row = np.zeros(input_grid.shape[1],dtype=int)
        output_grid = np.vstack((output_grid,new_row))
    
    #fill in blue region
    row_start = blue_height + empty_rows_above
    row_end = row_start+rows_to_add
    
    col_start = min_col
    col_end = col_start + blue_width
    
    output_grid[row_start:row_end, col_start:col_end] = 1

    return output_grid.tolist()
```
