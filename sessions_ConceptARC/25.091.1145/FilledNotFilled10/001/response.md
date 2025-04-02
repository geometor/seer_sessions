Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

def find_reachable_outside(grid, boundary_coords):
    """
    Performs a Breadth-First Search (BFS) starting from the grid borders
    to find all cells reachable without crossing the boundary. Excludes boundary cells themselves.

    Args:
        grid (np.array): The input grid.
        boundary_coords (set): A set of (row, col) tuples representing boundary cells.

    Returns:
        set: A set of (row, col) tuples representing non-boundary cells reachable from the outside.
    """
    rows, cols = grid.shape
    reachable = set()
    q = deque()
    visited = set(boundary_coords) # Treat boundary cells as initially visited (impassable walls)

    # Initialize queue with non-boundary cells on the border
    for r in range(rows):
        for c in [0, cols - 1]:
            coord = (r, c)
            if coord not in visited: # Check if it's already marked as boundary/visited
                # Note: Boundary cells CAN be on the border. We only start BFS from NON-boundary border cells.
                # find_reachable_outside is only interested in non-boundary cells reachable from outside.
                # So, if a border cell is not part of the boundary itself, add it.
                if coord not in boundary_coords:
                    q.append(coord)
                    reachable.add(coord)
                visited.add(coord) # Mark border cell visited regardless

    for c in range(1, cols - 1): # Avoid double-checking corners
        for r in [0, rows - 1]:
             coord = (r, c)
             if coord not in visited:
                if coord not in boundary_coords:
                     q.append(coord)
                     reachable.add(coord)
                visited.add(coord)

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_coord = (nr, nc)
                # Check if neighbor has not been visited
                if neighbor_coord not in visited
---
