# 9edfc990 • 004 • example_1 • investigate_coder

---
```python
"""
Replaces '0' (white) pixels with '1' (blue) pixels if they are adjacent to a non-zero pixel. This change propagates outwards.
There is an exception: pixels on the border should not be transformed if 0.
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
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    changed = True

    while changed:
        changed = False
        for row in range(rows):
            for col in range(cols):
                # Apply border condition:
                # if on border, skip, unless we are processing a swap.
                if (row == 0 or row == rows-1 or col == 0 or col == cols -1) and output_grid[row,col] == 0:
                    continue

                if output_grid[row, col] == 0:
                    neighbors = get_neighbors(output_grid, row, col)
                    for n_row, n_col in neighbors:
                        if output_grid[n_row, n_col] != 0:
                            output_grid[row, col] = 1
                            changed = True
                            break # need to break and restart to correctly propagate the change.
    return output_grid
```
