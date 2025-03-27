```python
import numpy as np
from collections import deque

"""
Identify all regions of white pixels (0) that are completely enclosed by azure pixels (8). 
Change the color of these enclosed white pixels to red (2). 
Leave all other pixels (azure pixels and white pixels connected to the grid boundary) unchanged.
"""

def find_reachable_white_pixels(grid):
    """
    Performs a BFS starting from boundary white pixels to find all white pixels
    reachable from the boundary.
    """
    height, width = grid.shape
    reachable = np.zeros_like(grid, dtype=bool) # Tracks reachable white pixels
    q = deque()

    # Add all boundary white pixels to the queue and mark as reachable
    for r in range(height):
        for c in [0, width - 1]: # Left and right edges
            if grid[r, c] == 0 and not reachable[r, c]:
                q.append((r, c))
                reachable[r, c] = True
    for c in range(width):
        for r in [0, height - 1]: # Top and bottom edges
             if grid[r, c] == 0 and not reachable[r, c]:
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If neighbor is white and not yet marked as reachable
                if grid[nr, nc] == 0 and not reachable[nr, nc]:
                    reachable[nr, nc] = True
                    q.append((nr, nc))

    return reachable


def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions with red.

    Args:
        input_grid (np.array): The input 2D numpy array representing the grid.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all white pixels reachable from the boundary
    reachable_white = find_reachable_white_pixels(input_grid)

    # Iterate through the grid
    for r in range(height):
        for c in range(width):
            # If a pixel is white in the input grid but not reachable from the boundary
            if input_grid[r, c] == 0 and not reachable_white[r, c]:
                # Change its color to red in the output grid
                output_grid[r, c] = 2

    return output_grid
```