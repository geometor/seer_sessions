# e8dc4411 • 008 • refine_coder

---
```python
"""
1.  **Identify Existing Red Diagonals:** Examine the input grid to find any existing diagonal lines of red (color 2) pixels. A diagonal is a sequence of contiguous red pixels extending downwards and to the right.
2.  **Determine Starting Point:**
    *   If no red diagonal is found, the input grid is returned as is.
    *   If a red diagonal *is* found, locate the last pixel (bottom-rightmost) of that diagonal. The new diagonal will start one row below and one column to the right of this pixel.
3.  **Extend New Diagonal:** Starting from the determined starting point, change the color of cells to red (color 2) diagonally downwards and to the right.
4.  **Terminate at Edge:** Continue this diagonal extension until either the bottom edge or the right edge of the grid is reached.
5.  **Preservation:** All other cells that do not fall under this rule remain the same from the input.
"""

import numpy as np

def find_last_pixel_of_diagonal(grid, color):
    """Finds the last pixel of the longest red diagonal."""
    last_pixel = None
    max_length = 0

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color:
                length = 0
                row, col = r, c
                while row < grid.shape[0] and col < grid.shape[1] and grid[row, col] == color:
                    length += 1
                    row += 1
                    col += 1

                if length > max_length:
                    max_length = length
                    last_pixel = (row - 1, col - 1)  # Last pixel of the diagonal

    return last_pixel

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Find the last pixel of the longest red diagonal.
    last_pixel = find_last_pixel_of_diagonal(input_grid, 2)

    if last_pixel is None:  # No red diagonal found
        return output_grid

    # Determine the starting point for the new diagonal.
    start_row, start_col = last_pixel
    start_row += 1
    start_col += 1

    # Extend the new diagonal.
    while start_row < output_grid.shape[0] and start_col < output_grid.shape[1]:
        output_grid[start_row, start_col] = 2
        start_row += 1
        start_col += 1

    return output_grid
```
