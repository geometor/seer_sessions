# 6c434453 • 012 • refine_coder

---
```python
"""
Transforms an input grid based on the following rule:

1.  **Identify Blue Blocks:** Find all contiguous regions of blue pixels.  Contiguous means connected horizontally or vertically (not diagonally).
2.  **Transform:** Change *all* blue pixels within the identified blue blocks to red.
3.  **Output:** The output grid is the result of this transformation.  All originally blue pixels are now red; other colors remain the same.
"""

import numpy as np

def get_neighbors(grid, r, c):
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def find_contiguous_blue(grid):
    rows, cols = grid.shape
    visited = set()
    blue_blocks = []

    def dfs(r, c, current_block):
        if (r, c) in visited or grid[r, c] != 1:
            return
        visited.add((r, c))
        current_block.append((r, c))
        for nr, nc in get_neighbors(grid, r, c):
            dfs(nr, nc, current_block)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 1 and (r, c) not in visited:
                current_block = []
                dfs(r, c, current_block)
                blue_blocks.append(current_block)
    return blue_blocks


def transform(input_grid):
    # Initialize output_grid with the same values as the input
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape

    # Find all contiguous blue blocks
    blue_blocks = find_contiguous_blue(input_grid)

    # Change all blue pixels in the blocks to red
    for block in blue_blocks:
        for r, c in block:
            output_grid[r, c] = 2

    return output_grid
```
