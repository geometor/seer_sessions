# 7447852a • 005 • refine_coder

---
```python
"""
1.  **Identify:** Find all white pixels (value 0) in the input grid.
2.  **Check Adjacency:** For each white pixel, check its immediate neighbors (up, down, left, and right).
3.  **Transform:** If any of the neighboring pixels are red (value 2), change the color of the white pixel to yellow (value 4).
4.  **Output:** The output grid is the modified input grid with the color changes.
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
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Identify white pixels
    white_pixels = [(r, c) for r in range(rows) for c in range(cols) if input_grid[r, c] == 0]

    # change output pixels based on adjacency to red
    for r, c in white_pixels:
        neighbor_coords = get_neighbors(input_grid, r, c)
        for nr, nc in neighbor_coords:
            if input_grid[nr, nc] == 2:  # Check if neighbor is red
                output_grid[r, c] = 4  # change to yellow
                break # only need one red neighbor

    return output_grid.tolist()
```
