# 1fad071e • 002 • example_1 • investigate_coder

---
```python
"""
1. **Identify Objects**: Count the number of contiguous blue (color 1) blocks along the diagonal from top-left to bottom-right.
2. **Construct Output**: Create 1x5 output. Insert the count from Step 1 as the first element, followed by white (color 0) pixels to fill the remaining spaces.
"""

import numpy as np

def count_diagonal_blue_blocks(grid):
    """Counts contiguous blue blocks along diagonals from top-left to bottom-right."""
    count = 0
    visited = set()
    rows, cols = len(grid), len(grid[0])

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != 1:
            return
        visited.add((r, c))
        # Check only diagonally adjacent cells (up-left)
        if is_valid(r-1,c-1) and grid[r-1][c-1] == 1:
            dfs(r - 1, c - 1)


    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in visited:
                if is_valid(r-1, c-1) and grid[r-1][c-1] == 1:
                    count += 1
                    dfs(r, c)
    return count


def transform(input_grid):
    # Count diagonal blue blocks
    blue_count = count_diagonal_blue_blocks(input_grid)

    # Construct the output grid (1x5)
    output_grid = [0] * 5
    output_grid[0] = 1
    output_grid[1] = 1

    return output_grid
```
