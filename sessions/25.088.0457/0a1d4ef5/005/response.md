Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque

"""
Identifies all solid, monochromatic, non-white rectangles within the input grid.
Sorts these rectangles based on their top-left corner coordinates (first by row, then by column).
Extracts the colors of the sorted rectangles.
Determines the dimensions (R, C) for the output grid such that R * C equals the total number of rectangles found (N), 
the absolute difference |R - C| is minimized, and R is minimized in case of ties.
Arranges the extracted colors into the R x C output grid in row-major order.
"""

def _find_connected_component(grid, start_row, start_col, visited):
    """
    Finds a connected component of the same color starting from (start_row, start_col).
    Uses Breadth-First Search (BFS) with 4-way adjacency (up, down, left, right).
    Returns the color, a set of pixel coordinates (as tuples) for the component, 
    and updates the visited matrix. Returns None for color and pixels if the 
    starting point is background (0) or already visited.

    Args:
        grid (np.ndarray): The input grid.
        start_row (int): The starting row index.
        start_col (int): The starting column index.
        visited (np
---
