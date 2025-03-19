# 42a50994 • 024 • refine_coder

---
```python
"""
Filters pixels in a grid, keeping only those with at least two neighbors of the same color (including diagonals).
"""

import numpy as np

def count_neighbors(grid, row, col):
    """Counts neighbors with the same color, including diagonals."""
    rows, cols = grid.shape
    target_color = grid[row, col]
    count = 0
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row or j != col) and grid[i, j] == target_color:
                count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid by removing pixels that have fewer than two neighbors of the same color.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Iterate through each pixel in the input grid.
    for row in range(rows):
        for col in range(cols):
            # Count neighbors of the same color, including diagonals.
            neighbor_count = count_neighbors(input_grid, row, col)
            # If fewer than two neighbors, change to white (0).
            if neighbor_count < 2:
                output_grid[row, col] = 0

    return output_grid
```

