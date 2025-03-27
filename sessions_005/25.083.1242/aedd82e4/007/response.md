```python
"""
1.  **Object Identification:** Identify all red (value 2) and white (value 0) pixels in the input grid.

2.  **Adjacency Check:** For *every* red pixel, check if it is adjacent (horizontally, vertically, or diagonally) to at least one white pixel.

3.  **Transformation:** If a red pixel is adjacent to any white pixel, change its color to blue (value 1). There is no prioritization; *all* red pixels meeting the adjacency condition are transformed.

4.  **Output:** Return the modified grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """Gets the values of adjacent pixels (including diagonals)."""
    rows, cols = grid.shape
    adjacent = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i, j) != (row, col):
                adjacent.append((i, j, grid[i, j]))
    return adjacent

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    red_pixels = []

    # Find all red pixels
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 2:
                red_pixels.append((r, c))


    # Iterate through red pixels and check for adjacency
    for r, c in red_pixels:
        adjacent_pixels = get_adjacent_pixels(output_grid, r, c)
        for ar, ac, val in adjacent_pixels:
            if val == 0:
                # change output pixels
                output_grid[r, c] = 1
                break  # Move to the next red pixel after changing

    return output_grid
```