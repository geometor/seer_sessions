# 810b9b61 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify:** Locate all blue (1) pixels in the input grid.
2.  **Conditional Replacement**: For each blue pixel:
    *   If the blue pixel is part of a contiguous block of 2 or more blue pixels (horizontally, vertically *or* diagonally connected), change it to a green pixel.
3.  **Preserve**: White pixels remain unchanged.
"""

import numpy as np

def is_part_of_block(grid, row, col):
    """
    Checks if a blue pixel at (row, col) is part of a contiguous block of 2 or more blue pixels.
    """
    color = grid[row, col]
    if color != 1:
        return False

    rows, cols = grid.shape
    count = 0

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
                count += 1
    
    return count > 0 # must connect to at least 1 neighbor.

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels 
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 1:
                if is_part_of_block(input_grid, row, col):
                    output_grid[row, col] = 3

    return output_grid
```
