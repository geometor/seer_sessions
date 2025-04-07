```python
"""
Transforms an input grid based on enclosed regions.

1. Initialize an output grid with the same dimensions as the input grid, filled entirely with zeros.
2. Identify all cells in the input grid that contain the value 0 and are located on the outermost border (edge) of the grid.
3. Perform a Breadth-First Search (BFS) starting from these border '0' cells. The search can only move horizontally or vertically to adjacent cells that also contain 0. Mark all reachable '0' cells during this search as 'exterior'.
4. Iterate through the entire input grid.
5. If an input cell contains a '0' and was *not* marked as 'exterior' during the BFS, it means this cell is part of an enclosed region. Set the corresponding cell in the output grid to 7.
6. All other cells in the output grid (those corresponding to input '1's or '0's marked as 'exterior') remain 0.
7. Return the final output grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills enclosed regions defined by '1's in the input grid with '7's.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # Initialize output_grid with zeros, same dimensions as input
    output_grid = np.zeros_like(input_array)

    # Create a visited grid to keep track of exterior '0' cells reached from the border
    visited = np.zeros_like(input_array, dtype=bool)
    queue = deque()

    # Helper function to check if a coordinate is within grid bounds
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # --- Find and mark exterior '0' cells using BFS starting from the border ---

    # Add all '0' cells on the border to the queue and mark as visited
    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and input_array[r, c] == 0 and not visited[r, c]:
                queue.append((r, c))
                visited[r, c] = True

    # Perform BFS
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is valid, is a '0' in input, and hasn't been visited
            if is_valid(nr, nc) and input_array[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                queue.append((nr, nc))

    # --- Fill the enclosed regions in the output grid ---

    # Iterate through the entire grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is '0' in the input and was *not* visited (i.e., not reachable from the border)
            if input_array[r, c] == 0 and not visited[r, c]:
                # Mark it as 7 in the output grid (it's an enclosed '0')
                output_grid[r, c] = 7
            # Else:
            # - If input was '1', output remains 0.
            # - If input was '0' and visited, output remains 0.

    # Convert numpy array back to list of lists for the final output
    return output_grid.tolist()
```