# 7447852a • 012 • refine_coder

---
```python
"""
Transforms an input grid by changing the last red pixel in each contiguous group of red pixels on a row to yellow, and then propagating the yellow color downwards if the cell below is not red.
"""

import numpy as np

def get_red_pixels(grid):
    # use where to find red pixels
    red_pixels = np.where(grid == 2)
    # combine and return list of (row, col)
    return list(zip(red_pixels[0], red_pixels[1]))

def get_red_groups(red_pixels_by_row):
    grouped_red_pixels = {}
    for row, cols in red_pixels_by_row.items():
        grouped_red_pixels[row] = []
        current_group = []
        cols.sort()  # Ensure columns are sorted
        for i in range(len(cols)):
            current_group.append(cols[i])
            if i + 1 == len(cols) or cols[i+1] != cols[i] + 1: # Check for contiguity
                grouped_red_pixels[row].append(current_group)
                current_group = []
    return grouped_red_pixels

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    red_pixels = get_red_pixels(input_grid)
    
    # create dictionary, keys are row, values are column
    red_pixels_by_row = {}
    for r, c in red_pixels:
        if r not in red_pixels_by_row:
            red_pixels_by_row[r] = []
        red_pixels_by_row[r].append(c)

    # group red pixels
    red_groups = get_red_groups(red_pixels_by_row)


    # change last red to yellow
    for row in red_groups:
      for group in red_groups[row]:
        last_red_col = group[-1]
        output_grid[row, last_red_col] = 4


    # propagate yellow color down, conditionally
    for r in range(rows - 1):
        for c in range(cols):
            if output_grid[r, c] == 4:
                if output_grid[r + 1, c] != 2:
                    output_grid[r + 1, c] = 4

    return output_grid
```
