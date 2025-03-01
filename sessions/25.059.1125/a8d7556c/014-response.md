# a8d7556c • 014 • refine_coder

---
```python
"""
The transformation involves changing white pixels to red if they are adjacent to grey pixels and form enclosed interior spaces. A space is considered enclosed if it's completely surrounded by grey pixels, meaning there's no path from a white pixel within the space to the edge of the grid via other white pixels.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Returns the coordinates of valid neighbors (up, down, left, right) of a pixel."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))  # Up
    if r < rows - 1:
        neighbors.append((r + 1, c))  # Down
    if c > 0:
        neighbors.append((r, c - 1))  # Left
    if c < cols - 1:
        neighbors.append((r, c + 1))  # Right
    return neighbors

def is_fully_enclosed(grid, r, c, visited):
    """
    Checks if a white pixel is part of a fully enclosed region using a depth-first search.
    A region is considered fully enclosed if all paths from the starting pixel to the grid edge are blocked by grey pixels.
    """
    rows, cols = grid.shape

    # Base cases:
    # 1. Reached the edge of the grid: not enclosed.
    if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
        if grid[r,c] == 0: # boundary and white
           return False

    visited.add((r, c))
    neighbors = get_neighbors(grid, r, c)

    for nr, nc in neighbors:
        if (nr, nc) not in visited:
            if grid[nr, nc] == 0:  # White neighbor
                if not is_fully_enclosed(grid, nr, nc, visited):
                    return False  # If a neighbor is not enclosed, neither is this pixel
            # We don't need an explicit check for grey pixels here. If it's grey, the recursion stops on this path.

    return True  # All paths are blocked by grey pixels


def transform(input_grid):
    """
    Transforms the input grid by changing white pixels to red based on adjacency to grey
    and full enclosure within grey boundaries.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through all pixels
    for r in range(rows):
        for c in range(cols):
            # Process only white pixels
            if input_grid[r, c] == 0:
                # Check for adjacency to grey
                is_adjacent = False
                for nr, nc in get_neighbors(input_grid, r, c):
                    if input_grid[nr, nc] == 5:
                        is_adjacent = True
                        break

                # If adjacent to grey, check for full enclosure
                if is_adjacent:
                    visited = set()
                    if is_fully_enclosed(input_grid, r, c, visited):
                        output_grid[r, c] = 2  # Change to red

    return output_grid
```
