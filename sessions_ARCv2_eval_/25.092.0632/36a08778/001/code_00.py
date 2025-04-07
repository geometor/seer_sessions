import numpy as np
from collections import deque

"""
Identify all orange (7) pixels in the input grid that are connected to any edge of the grid via a path consisting only of adjacent (up, down, left, right) orange pixels. Red (2) and magenta (6) pixels act as impassable barriers. Change any orange (7) pixel that is *not* connected to an edge in this way to magenta (6). Leave all other pixels (red, original magenta, edge-connected orange) unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the described rule.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid = np.copy(input_np) # Initialize output grid as a copy

    # Create a grid to track visited/safe orange pixels
    visited = np.zeros_like(input_np, dtype=bool)
    q = deque()

    # Find initial orange pixels connected to the edge
    for r in range(rows):
        # Check left edge
        if input_np[r, 0] == 7 and not visited[r, 0]:
            q.append((r, 0))
            visited[r, 0] = True
        # Check right edge
        if input_np[r, cols - 1] == 7 and not visited[r, cols - 1]:
            q.append((r, cols - 1))
            visited[r, cols - 1] = True

    for c in range(cols):
        # Check top edge
        if input_np[0, c] == 7 and not visited[0, c]:
            q.append((0, c))
            visited[0, c] = True
        # Check bottom edge
        if input_np[rows - 1, c] == 7 and not visited[rows - 1, c]:
            q.append((rows - 1, c))
            visited[rows - 1, c] = True

    # Perform BFS (flood fill) from edge-connected orange pixels
    while q:
        r, c = q.popleft()

        # Check 4 adjacent neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is orange and not visited
                if input_np[nr, nc] == 7 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Iterate through the grid and change unconnected orange pixels to magenta
    for r in range(rows):
        for c in range(cols):
            # If it's an orange pixel but wasn't visited (not connected to edge)
            if input_np[r, c] == 7 and not visited[r, c]:
                output_grid[r, c] = 6 # Change to magenta

    return output_grid.tolist()