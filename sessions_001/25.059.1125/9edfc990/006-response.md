# 9edfc990 • 006 • refine_coder

---
```python
"""
Replaces '0' (white) pixels with another color if they are adjacent to a specific "seed" color. 
The seed and fill colors are determined by analyzing the examples. This change propagates outwards, filling all reachable '0' pixels.
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

def transform(input_grid, seed_colors=[1, 5], fill_color=1):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    changed = True

    while changed:
        changed = False
        grid_copy = np.copy(output_grid)  # Work on a copy during each iteration
        for row in range(rows):
            for col in range(cols):
                # Apply border condition:
                # if on border, skip, unless we are processing a swap.
                if (row == 0 or row == rows-1 or col == 0 or col == cols -1) and grid_copy[row,col] == 0:
                    continue

                if grid_copy[row, col] == 0:
                    neighbors = get_neighbors(grid_copy, row, col)
                    for n_row, n_col in neighbors:
                        if grid_copy[n_row, n_col] in seed_colors:
                            output_grid[row, col] = fill_color
                            changed = True
                            break  # Break inner loop, but continue propagation
        if not changed:
            break # No changes, stop the loop

    return output_grid
```
