```python
"""
1.  **Identify the border:** Find all pixels that constitute the outer perimeter of the input grid. This includes all pixels in the first and last rows, as well as all pixels in the first and last columns.
2.  **Identify the center:** Find the coordinate of the pixel in the very center
    of the grid.
3.  **Transform the border:** Change the color (value) of all border pixels in
    the output grid to 0 (white).
4.  **Retain inner grid:** For every other pixel, retain the original color if
    it is in the center, else flip the pixel with its complement position on the
    opposite side. For odd grids, this is the pixel mirrored across the center.
    For even grids, this will mean two pixels on opposite sides will have their
    values swapped.
"""

import numpy as np

def get_border_indices(grid):
    rows, cols = grid.shape
    border_indices = []
    for r in range(rows):
        for c in range(cols):
            if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                border_indices.append((r, c))
    return border_indices

def get_center_index(grid):
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return (center_row, center_col)
    
def get_complement_index(grid, r, c):
    rows, cols = grid.shape
    complement_r = rows - 1 - r
    complement_c = cols - 1 - c
    return (complement_r, complement_c)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # change border pixels to 0
    border_indices = get_border_indices(input_grid)
    for r, c in border_indices:
        output_grid[r, c] = 0

    # get center index
    center_row, center_col = get_center_index(input_grid)
    
    # swap non-border, non-center pixels    
    for r in range(rows):
        for c in range(cols):
            if (r,c) not in border_indices and (r, c) != (center_row, center_col) :
                cr, cc = get_complement_index(input_grid, r, c)
                output_grid[r,c] = input_grid[cr, cc]
                output_grid[cr, cc] = input_grid[r, c]

    return output_grid.tolist()
```