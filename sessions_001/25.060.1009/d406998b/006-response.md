# d406998b • 006 • refine_coder

---
```python
"""
A gray pixel changes to green if and only if it is horizontally or vertically adjacent to exactly two gray pixels and one white pixel, or one gray pixel and two white pixels.
"""

import numpy as np

def get_hv_adjacent_pixels(grid, row, col):
    """Gets values of horizontally/vertically adjacent pixels."""
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append(grid[row-1, col]) # Up
    if row < rows - 1:
        adjacent.append(grid[row+1, col]) # Down
    if col > 0:
        adjacent.append(grid[row, col-1]) # Left
    if col < cols - 1:
        adjacent.append(grid[row, col+1]) # Right
    return adjacent

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 5:  # Check if the pixel is gray
                hv_adjacent = get_hv_adjacent_pixels(input_grid, row, col)
                gray_count = hv_adjacent.count(5)
                white_count = hv_adjacent.count(0)

                # if input_grid[row, col] == 5 is HV adjacent to exactly two 5 and one 0, or one 5 and two 0:
                if (gray_count == 2 and white_count == 1) or (gray_count == 1 and white_count == 2):
                    output_grid[row, col] = 3  # Change to green

    return output_grid
```
