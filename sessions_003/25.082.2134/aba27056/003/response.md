```python
"""
Fill enclosed regions of '0' (white) pixels with '4' (yellow), leaving other regions unchanged.
"""

import numpy as np

def get_neighbors(grid, r, c):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if r > 0:
        neighbors.append((r - 1, c))
    if r < rows - 1:
        neighbors.append((r + 1, c))
    if c > 0:
        neighbors.append((r, c - 1))
    if c < cols - 1:
        neighbors.append((r, c + 1))
    return neighbors

def is_enclosed(grid, start_r, start_c):
    """Checks if a region of '0's is fully enclosed by non-'0's."""
    rows, cols = grid.shape
    visited = set()
    to_visit = [(start_r, start_c)]
    on_boundary = False

    while to_visit:
        r, c = to_visit.pop()

        if (r, c) in visited:
            continue
        visited.add((r, c))

        if grid[r, c] != 0:
            continue
        
        # Check if the current cell is on the boundary
        if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
            on_boundary = True

        neighbors = get_neighbors(grid, r, c)
        for nr, nc in neighbors:
            if (nr, nc) not in visited:
                to_visit.append((nr, nc))

    return not on_boundary, visited



def transform(input_grid):
    """Transforms the input grid according to the rule."""
    input_grid = np.array(input_grid)  # Convert to NumPy array
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate and find the enclosed regions
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 0:
                enclosed, visited = is_enclosed(input_grid, r, c)
                if enclosed:
                    for vr, vc in visited:
                        output_grid[vr, vc] = 4
    return output_grid.tolist()
```