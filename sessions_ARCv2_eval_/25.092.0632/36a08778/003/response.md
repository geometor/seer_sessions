```python
import numpy as np
from collections import deque

"""
Identify all orange (7) pixels in the input grid that are connected to any edge of the grid via a path consisting only of adjacent (up, down, left, right) orange pixels. Red (2) and magenta (6) pixels act as impassable barriers. Change any orange (7) pixel that is *not* connected to an edge in this way to magenta (6). Leave all other pixels (red, original magenta, edge-connected orange) unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the flood fill rule from edges.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # Create a grid to track orange pixels connected to the edge
    is_connected_to_edge = np.zeros_like(input_np, dtype=bool)

    # Initialize a queue for Breadth-First Search (BFS)
    q = deque()

    # Seed the BFS with orange pixels on the edges
    for r in range(rows):
        # Check left edge
        if input_np[r, 0] == 7 and not is_connected_to_edge[r, 0]:
            is_connected_to_edge[r, 0] = True
            q.append((r, 0))
        # Check right edge
        if input_np[r, cols - 1] == 7 and not is_connected_to_edge[r, cols - 1]:
            is_connected_to_edge[r, cols - 1] = True
            q.append((r, cols - 1))

    for c in range(cols): # Avoid double-counting corners already checked
        # Check top edge
        if input_np[0, c] == 7 and not is_connected_to_edge[0, c]:
            is_connected_to_edge[0, c] = True
            q.append((0, c))
        # Check bottom edge
        if input_np[rows - 1, c] == 7 and not is_connected_to_edge[rows - 1, c]:
            is_connected_to_edge[rows - 1, c] = True
            q.append((rows - 1, c))

    # Perform BFS (flood fill) from edge-connected orange pixels
    while q:
        r, c = q.popleft()

        # Check 4 adjacent neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is orange (7) and hasn't been visited yet
                if input_np[nr, nc] == 7 and not is_connected_to_edge[nr, nc]:
                    # Mark as connected and add to queue for further exploration
                    is_connected_to_edge[nr, nc] = True
                    q.append((nr, nc))

    # Iterate through the grid and change unconnected orange pixels to magenta
    for r in range(rows):
        for c in range(cols):
            # If it's an orange pixel in the input AND it wasn't reached by the BFS (not connected)
            if input_np[r, c] == 7 and not is_connected_to_edge[r, c]:
                # Change its color to magenta (6) in the output grid
                output_grid[r, c] = 6

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```