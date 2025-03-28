# 32597951 • 016 • example_3 • investigate_coder

---
```python
"""
1. Identify Azure Regions: Locate all contiguous regions of azure (8) pixels within the input grid.
2. Identify original blue(1) pixels adjacent to any azure pixel(8): For each azure pixel, find the blue pixels that are directly adjacent (up, down, left, or right) to original azure(8).
3. Transform Pixels: Transform those identified blue pixels(1) into green(3)
4. Preserve Other Pixels: All other pixels in the grid remain unchanged. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all azure (8) pixels
    azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 8:
                azure_pixels.append((r, c))

    # Find adjacent blue (1) pixels and change them to green (3)
    for r, c in azure_pixels:
        for nr, nc in get_neighbors(input_grid, r, c):
            if input_grid[nr, nc] == 1:
                output_grid[nr, nc] = 3

    return output_grid
```
