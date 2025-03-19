# 941d9a10 • 016 • example_3 • investigate_coder

---
```python
"""
The transformation identifies columns of 5s. For 5's columns that extend from top section down to the center horizontal row, a '1' is placed at the top adjacent 0. For '5's that appear on the center horizontal, the adjacent '0' to the right is changed to a `2`. For 5 columns in the bottom section that don't connect to the center row, place a '3' at the bottom-most, adjacent '0'. Other cells appear to retain their original values.
"""

import numpy as np

def get_top_change_coords(input_grid):
    rows, cols = input_grid.shape
    mid_row = rows // 2
    coords = []

    for c in range(cols):
        if input_grid[mid_row-1][c] == 5:
            for r in range(mid_row):
                if input_grid[r][c] == 0:
                    coords.append((r,c))
                    break # only want first one

    return coords
                

def get_center_change_coords(input_grid):
    rows, cols = input_grid.shape
    mid_row = rows // 2
    
    coords = None
    for c in range(cols):
        if input_grid[mid_row-1][c] == 5 and input_grid[mid_row][c] == 5:
            if input_grid[mid_row-1][c+1] == 0 and input_grid[mid_row][c+1] == 0:
                coords = (mid_row-1, c+1) # take the first row as where to put it
                break; # right most

    return coords

def get_bottom_change_coords(input_grid):
    rows, cols = input_grid.shape
    mid_row = rows // 2
    coords = []

    for c in range(cols):
        if input_grid[rows-1][c] == 5 and input_grid[mid_row-1][c] != 5:
            for r in range(rows -1, mid_row-1, -1):
                if input_grid[r][c] == 0:
                    coords.append((r,c))
                    break # only want last one
    return coords


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Top Modification
    top_coords = get_top_change_coords(input_grid)
    for r, c in top_coords:
       output_grid[r][c] = 1
    
    # center
    center_coords = get_center_change_coords(input_grid)
    if center_coords:
        r, c = center_coords
        output_grid[r][c] = 2
        output_grid[r+1][c] = 2

    # Bottom Modification
    bot_coords = get_bottom_change_coords(input_grid)
    for r, c in bot_coords:
        output_grid[r][c] = 3

    return output_grid
```
