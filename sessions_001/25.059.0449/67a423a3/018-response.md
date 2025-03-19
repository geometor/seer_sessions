# 67a423a3 • 018 • refine_coder

---
```python
"""
1.  **Identify** the blue (1) square object in the input grid, located at the center.
2.  **Locate** all pixels directly adjacent (up, down, left, right - not diagonally) to the blue square.
3.  **Change** the color of adjacent pixels that are white (0) to yellow (4).
4. **Preserve** the color of the blue pixels.
5. **Preserve** all other pixels, including the outermost layer of the grid.
6.  **Output** the modified grid.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the coordinates of directly adjacent pixels (up, down, left, right).
    """
    rows, cols = grid.shape
    adjacent_pixels = []
    if row > 0:
        adjacent_pixels.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_pixels.append((row + 1, col))  # Down
    if col > 0:
        adjacent_pixels.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_pixels.append((row, col + 1))  # Right
    return adjacent_pixels

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels in the grid
    for row in range(rows):
        for col in range(cols):
            # Identify blue (1) pixels
            if input_grid[row, col] == 1:
                # Locate adjacent pixels
                adjacent_pixels = get_adjacent_pixels(input_grid, row, col)
                # Change adjacent pixels from white (0) to yellow (4)
                for adj_row, adj_col in adjacent_pixels:
                    if input_grid[adj_row, adj_col] == 0:
                        output_grid[adj_row, adj_col] = 4

    return output_grid
```
