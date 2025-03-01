# 8e5a5113 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation involves replacing the white and grey regions with the colors adjacent to them. The left-most and right-most colors fill the 'background'.
"""

import numpy as np

def get_adjacent(grid, r, c):
    rows, cols = grid.shape
    adjacent_pixels = []

    if r > 0:
        adjacent_pixels.append((r - 1, c, grid[r-1,c]))  # Up
    if r < rows - 1:
        adjacent_pixels.append((r + 1, c, grid[r+1, c]))  # Down
    if c > 0:
        adjacent_pixels.append((r, c-1, grid[r, c-1])) # Left
    if c < cols - 1:
        adjacent_pixels.append((r, c+1, grid[r, c+1]))  # Right
    
    return adjacent_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 0:
                adjacent = get_adjacent(input_grid,r,c)
                #check horizontal and vertical for same
                adj_vals = [pixel for _, _, pixel in adjacent]
                #get left/right (horizontal)
                horz = []
                if c > 0:
                    horz.append(input_grid[r,c-1])
                if c < cols - 1:
                    horz.append(input_grid[r,c+1])
                if len(set(horz)) == 1 and len(horz)>0:
                    if c > 0:
                        output_grid[r,c-1] = horz[0]

            if input_grid[r,c] == 5:
                adjacent = get_adjacent(input_grid,r,c)
                #check horizontal and vertical for same
                adj_vals = [pixel for _, _, pixel in adjacent]
                #get left/right (horizontal)
                horz = []
                if r > 0:
                    horz.append(input_grid[r-1,c])
                if r < rows - 1:
                    horz.append(input_grid[r+1,c])
                if len(set(horz)) == 1 and len(horz)>0:
                    if r > 0:
                        output_grid[r-1,c] = horz[0]

    return output_grid
```
