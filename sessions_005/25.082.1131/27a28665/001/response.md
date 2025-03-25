```python
"""
Counts the number of distinct regions of connected non-zero pixels in a 2D grid.
Two non-zero pixels are part of the same region if they have the same value
and are directly adjacent (horizontally or vertically).
"""

import numpy as np

def is_valid(r, c, grid):
    """Checks if a given row and column are within the grid bounds."""
    rows, cols = len(grid), len(grid[0])
    return 0 <= r < rows and 0 <= c < cols

def dfs(r, c, grid, visited, color):
    """Performs Depth-First Search to mark all connected pixels of the same color."""
    rows, cols = len(grid), len(grid[0])
    
    # Check boundary conditions and if already visited or it's not the correct color
    if not is_valid(r,c,grid) or (r, c) in visited or grid[r][c] != color:
        return

    visited.add((r, c))

    # Recursively visit adjacent cells (up, down, left, right)
    dfs(r + 1, c, grid, visited, color)
    dfs(r - 1, c, grid, visited, color)
    dfs(r, c + 1, grid, visited, color)
    dfs(r, c - 1, grid, visited, color)


def transform(input_grid):
    """Counts distinct regions of same-colored, orthogonally connected, non-zero pixels."""
    grid = input_grid
    rows, cols = len(grid), len(grid[0])
    visited = set()
    count = 0

    # Iterate through all cells of the grid
    for r in range(rows):
        for c in range(cols):
            # if unvisited and it is non-zero
            if (r, c) not in visited and grid[r][c] != 0:
                # Start a new DFS from this cell for a region of like colors
                dfs(r, c, grid, visited, grid[r][c])
                count += 1  # Increment region count

    return count
```