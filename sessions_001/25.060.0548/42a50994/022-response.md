# 42a50994 • 022 • example_4 • investigate_coder

---
```python
"""
Filters yellow pixels in a grid, keeping only those with at least three yellow neighbors.
"""

import numpy as np

def count_yellow_neighbors(grid, row, col):
    """Counts the number of yellow (4) neighbors around a given cell."""
    rows, cols = grid.shape
    count = 0
    # Check up, down, left, right
    if row > 0 and grid[row-1, col] == 4:
        count += 1
    if row < rows - 1 and grid[row+1, col] == 4:
        count += 1
    if col > 0 and grid[row, col-1] == 4:
        count += 1
    if col < cols - 1 and grid[row, col+1] == 4:
        count += 1
    return count

def transform(input_grid):
    """
    Transforms the input grid by removing yellow pixels that have fewer than three yellow neighbors.

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
            # Check if the current pixel is yellow.
            if input_grid[row, col] == 4:
                # Count yellow neighbors.
                yellow_neighbors = count_yellow_neighbors(input_grid, row, col)
                # If fewer than three yellow neighbors, change to white.
                if yellow_neighbors < 3:
                    output_grid[row, col] = 0

    return output_grid
```

