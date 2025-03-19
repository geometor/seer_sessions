# b2862040 • 022 • refine_coder

---
```python
"""
1.  **Identify** all maroon (9) pixels in the input grid.
2.  **For each** maroon (9) pixel, **check** if it is directly adjacent (above, below, left, or right, *not* diagonally) to at least one blue (1) pixel.
3. **If** a maroon pixel is adjacent to a blue pixel, **change** its color to grey (8).
4.  **Otherwise**, leave the maroon pixel's color unchanged.
5.  The output grid is the result of these color changes.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the adjacent pixels of a given cell in a grid.
    """
    rows, cols = grid.shape
    adjacent_pixels = []

    # Check above
    if row > 0:
        adjacent_pixels.append((row - 1, col))
    # Check below
    if row < rows - 1:
        adjacent_pixels.append((row + 1, col))
    # Check left
    if col > 0:
        adjacent_pixels.append((row, col - 1))
    # Check right
    if col < cols - 1:
        adjacent_pixels.append((row, col + 1))

    return adjacent_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # iterate all pixels
    for row in range(rows):
        for col in range(cols):
            # only evaluate maroon pixels
            if input_grid[row, col] == 9:
                # check adjacent pixels
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                for r, c in adjacent_pixels:
                    # change to grey if adjacent to blue
                    if input_grid[r, c] == 1:
                        output_grid[row, col] = 8
                        break  # Only need one adjacent blue pixel

    return output_grid
```
