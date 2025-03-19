# d406998b • 002 • example_1 • investigate_coder

---
```python
"""
Iterate through each pixel of the input grid. If a pixel's color is '5' (gray), check its adjacent pixels (up, down, left, and right). If at least two adjacent pixels are '0' (white), change the pixel's color to '3' (green). Otherwise, keep the original color.  Pixels that are '0' are copied to the output.
"""

import numpy as np

def count_adjacent_whites(grid, row, col):
    """Counts the number of white (0) adjacent pixels to a given cell."""
    rows, cols = grid.shape
    count = 0
    # Check up
    if row > 0 and grid[row-1, col] == 0:
        count += 1
    # Check down
    if row < rows - 1 and grid[row+1, col] == 0:
        count += 1
    # Check left
    if col > 0 and grid[row, col-1] == 0:
        count += 1
    # Check right
    if col < cols - 1 and grid[row, col+1] == 0:
        count += 1
    return count

def transform(input_grid):
    # Initialize output grid with the same dimensions and data type as the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel
    for row in range(rows):
        for col in range(cols):
            # If the pixel is gray (5)
            if input_grid[row, col] == 5:
                # Count adjacent white pixels
                white_count = count_adjacent_whites(input_grid, row, col)
                # If at least two adjacent pixels are white, change to green (3)
                if white_count >= 2:
                    output_grid[row, col] = 3
            # else the output grid already has the correct value from the np.copy

    return output_grid
```
