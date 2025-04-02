import numpy as np
from collections import deque

"""
Identify all contiguous regions composed exclusively of white (0) pixels.
For each identified white region, determine if it is completely enclosed by green (3) pixels. 
(A region is enclosed if every path from a pixel within the region to the edge of the grid passes through at least one green pixel).
If a white region is found to be completely enclosed by green pixels, change the color of all white (0) pixels within that specific enclosed region to yellow (4).
Leave all other pixels unchanged.
"""

def transform(input_grid):
    """
    Fills white (0) regions enclosed by green (3) pixels with yellow (4).

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # Visited array to keep track of pixels reachable from the border
    visited = np.zeros_like(grid, dtype=bool)
    
    # Queue for Breadth-First Search (BFS)
    q = deque()

    # Initialize BFS with all white pixels on the border
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r, c] == 0 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
            if grid[r, c] == 0 and not visited[r, c]:
                q.append((r, c))
                visited[r, c] = True

    # Perform BFS to find all white pixels reachable from the border
    while q:
        r, c = q.popleft()

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If the neighbor is white and not visited, add it to the queue
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white (0) and was not reached by the BFS (i.e., not visited)
            # it means it's part of an enclosed white region.
            if grid[r, c] == 0 and not visited[r, c]:
                # Change the color of this pixel to yellow (4) in the output grid
                output_grid[r, c] = 4

    # Convert back to list of lists before returning
    return output_grid.tolist()