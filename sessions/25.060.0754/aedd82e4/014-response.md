# aedd82e4 • 014 • refine_coder

---
```python
"""
1.  Find Red Pixels: Locate all pixels with the color red.
2.  Check Diagonal Adjacency: For each red pixel, examine its diagonally adjacent pixels.
3.  Conditional Color Change: If a diagonally adjacent pixel is white (color value 0), change that pixel's color to blue (color value 1). If there are no diagonally adjacent pixels, or if the adjacent pixels are not white, do not change those pixels.
"""

import numpy as np

def get_diagonally_adjacent_pixels(grid, row, col):
    # get all valid diagonally adjacent pixel coordinates for a given cell
    rows, cols = grid.shape
    adjacent_pixels = []
    for i in [-1, 1]:
        for j in [-1, 1]:
            new_row, new_col = row + i, col + j
            if 0 <= new_row < rows and 0 <= new_col < cols:
                adjacent_pixels.append((new_row, new_col))
    return adjacent_pixels

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel of input grid
    for row in range(rows):
        for col in range(cols):
            # find red pixels
            if input_grid[row, col] == 2:
                # Get diagonally adjacent pixels
                adjacent_pixels = get_diagonally_adjacent_pixels(input_grid, row, col)
                # change output pixels
                for r, c in adjacent_pixels:
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 1

    return output_grid
```
