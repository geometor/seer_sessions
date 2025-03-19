# 00d62c1b • 028 • example_5 • investigate_coder

---
```python
"""
The transformation rule is as follows:
1.  Preserve the background: White (0) pixels remain unchanged.
2.  Fill Interior: All green pixels that are not on the edge of a contiguous green object become yellow.
    In other words, if a green pixel is completely surrounded by other green pixels (not diagonally), it changes to yellow (4).
    Green pixels adjacent to any white pixel, remain green.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append(grid[row - 1, col])  # Up
    if row < rows - 1:
        neighbors.append(grid[row + 1, col])  # Down
    if col > 0:
        neighbors.append(grid[row, col - 1])  # Left
    if col < cols - 1:
        neighbors.append(grid[row, col + 1])  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is green (3)
            if input_grid[row, col] == 3:
                neighbors = get_neighbors(input_grid, row, col)
                # Check if all neighbors are also green (3)
                if all(neighbor == 3 for neighbor in neighbors):
                    output_grid[row, col] = 4  # Change to yellow (4)

    return output_grid
```
