```python
"""
Perform a flood fill starting from the white border cells of the input grid,
using the input azure (8) cells as impassable barriers. The area reachable
from the white border cells without crossing barriers is filled with azure (8)
in the output grid. All other cells, including the original barrier locations,
become white (0) in the output grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill from the white border cells, constrained by azure barriers.

    Args:
        input_grid (numpy.ndarray): A 2D numpy array representing the input grid.

    Returns:
        numpy.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid with white (0)
    output_grid = np.zeros((height, width), dtype=int)

    # Identify barrier locations (azure pixels in input)
    barrier_locations = set()
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 8:
                barrier_locations.add((r, c))

    # Initialize queue for Breadth-First Search (BFS) and visited set
    queue = deque()
    visited = set()

    # Seed the queue with white border cells
    for r in range(height):
        for c in [0, width - 1]: # Left and right borders
            if (r, c) not in barrier_locations and (r,c) not in visited:
                queue.append((r, c))
                visited.add((r, c))
                output_grid[r, c] = 8 # Mark reachable cell in output

    for c in range(width):
         for r in [0, height - 1]: # Top and bottom borders (avoid double-counting corners)
            if (r, c) not in barrier_locations and (r,c) not in visited:
                queue.append((r, c))
                visited.add((r, c))
                output_grid[r, c] = 8 # Mark reachable cell in output

    # Define 4-way adjacent neighbors
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill (BFS)
    while queue:
        r, c = queue.popleft()

        # Explore neighbors
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is not a barrier and has not been visited
                if (nr, nc) not in barrier_locations and (nr, nc) not in visited:
                    # Mark as visited and add to queue
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    # Set the corresponding cell in the output grid to azure (8)
                    output_grid[nr, nc] = 8

    # The output grid is now filled; barrier locations and unreachable areas remain white (0)
    return output_grid
```