import numpy as np
from collections import deque

"""
Performs a flood fill operation starting from white pixels (0) on the leftmost edge (column 0) of the grid. 
The fill color is red (2).
The fill propagates orthogonally (up, down, left, right) only to adjacent white pixels (0).
Blue pixels (1) and grid boundaries act as barriers, stopping the fill propagation.
Pixels that are reachable by this flood fill are changed to red (2) in the output grid.
"""

def transform(input_grid):
    """
    Applies a flood fill from the left edge, blocked by blue pixels.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()  # Initialize output_grid as a copy
    height, width = grid.shape

    # Constants for colors
    white = 0
    blue = 1
    red = 2

    # Keep track of visited pixels during the flood fill
    visited = np.zeros_like(grid, dtype=bool)

    # Queue for BFS (flood fill)
    queue = deque()

    # Initialize the queue with all white pixels in the first column (left edge)
    for r in range(height):
        if grid[r, 0] == white:
            if not visited[r, 0]:
                queue.append((r, 0))
                visited[r, 0] = True
                output_grid[r, 0] = red # Change starting pixels to red

    # Perform the flood fill (BFS)
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (in the original grid) and hasn't been visited
                # Blue pixels implicitly act as barriers because we only propagate through white
                if grid[nr, nc] == white and not visited[nr, nc]:
                    visited[nr, nc] = True
                    output_grid[nr, nc] = red # Change reachable white pixel to red
                    queue.append((nr, nc)) # Add neighbor to the queue to continue filling

    # Convert back to list of lists before returning
    return output_grid.tolist()