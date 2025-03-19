# 3aa6fb7a • 010 • example_2 • investigate_coder

---
```python
"""
The transformation replaces azure (8) pixels with blue (1) pixels if and only if the azure pixel has only one neighbor in the north, south, east, or west direction that is also azure. Otherwise, keep the azure color.
"""

import numpy as np

def count_adjacent_azure(grid, row, col):
    """Counts the number of adjacent azure pixels (excluding diagonals)."""
    count = 0
    rows, cols = grid.shape
    # Check North
    if row > 0 and grid[row-1, col] == 8:
        count += 1
    # Check South
    if row < rows - 1 and grid[row+1, col] == 8:
        count += 1
    # Check West
    if col > 0 and grid[row, col-1] == 8:
        count += 1
    # Check East
    if col < cols - 1 and grid[row, col+1] == 8:
        count += 1
    return count

def transform(input_grid):
    """Transforms the input grid according to the defined rule."""
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # Check if the pixel is azure
            if input_grid[row, col] == 8:
                # Count adjacent azure pixels
                adjacent_count = count_adjacent_azure(input_grid, row, col)
                # Replace with blue if only one adjacent azure pixel
                if adjacent_count == 1:
                    output_grid[row, col] = 1

    return output_grid
```
