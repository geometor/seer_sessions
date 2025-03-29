Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Transforms the grid based on object adjacency rules between blue (1) and azure (8).

1. Finds all contiguous objects (8-connectivity) of blue pixels and azure pixels.
2. For each blue object: If *every* pixel within that object is adjacent (8 neighbors)
   to at least one azure pixel, change all pixels of that blue object to red (2).
3. For each azure object: If *every* pixel within that object is adjacent (8 neighbors)
   to at least one blue pixel, change all pixels of that azure object to red (2).
4. Pixels not part of objects meeting these criteria retain their original color.
"""

# Helper function to check neighbors (8 neighbors: horizontal, vertical, diagonal)
def _has_neighbor_color(grid, r, c, target_color):
    """
    Checks if any of the 8 neighbors of cell (r, c) in the grid has the target_color.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the cell.
        c (int): Column index of the cell.
        target_color (int): The color to look for in neighbors.

    Returns:
        bool: True if a neighbor with target_color is found, False otherwise.
    """
    height, width = grid.shape
    # Iterate through all 8 neighbor offsets (dr, dc)
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue

            nr, nc = r + dr, c + dc

            # Check if the neighbor coordinates are within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor has the target color
                if grid[nr, nc] == target_color:
                    return True
    # No neighbor with the target color found
    return False

# Helper function to find contiguous objects (8-connectivity) of a specific color using BFS
def find_objects(grid, color):
    """
    Finds all contiguous objects of a given color in the grid using 8-way connectivity.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list
---
