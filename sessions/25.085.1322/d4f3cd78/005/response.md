```python
"""
Identifies white (0) pixels that are 'enclosed' by gray (5) pixels or grid boundaries and fills these enclosed areas with azure (8). A white pixel is considered enclosed if it cannot reach the grid border by traversing only adjacent white pixels. Gray pixels act as barriers.

1. Initialize the output grid as a copy of the input grid.
2. Identify 'exterior' white pixels: Perform a Breadth-First Search (BFS) starting from all white pixels located on the grid borders. This BFS can only traverse through other white pixels. Mark all reachable white pixels as 'visited'.
3. Fill 'interior' white pixels: Iterate through the entire grid. If a pixel was originally white (in the input grid) but was *not* marked as 'visited' by the border BFS, change its color to azure (8) in the output grid.
4. Return the modified output grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill transformation to enclosed white regions.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    rows, cols = input_grid.shape

    # Define colors
    WHITE = 0
    GRAY = 5  # Gray acts as a barrier in this logic
    AZURE = 8 # Fill color for enclosed white areas

    # --- Step 1: Initialize output grid ---
    output_grid = np.copy(input_grid)

    # --- Step 2: Identify 'exterior' white pixels using BFS ---

    # Boolean grid to mark white pixels reachable from the border via white paths
    visited_white_from_border = np.zeros_like(input_grid, dtype=bool)
    queue = deque()

    # Initialize the queue with all white border pixels
    for r in range(rows):
        for c in [0, cols - 1]: # Left and right borders
            if input_grid[r, c] == WHITE and not visited_white_from_border[r, c]:
                visited_white_from_border[r, c] = True
                queue.append((r, c))
    for c in range(1, cols - 1): # Top and bottom borders (excluding corners already checked)
         for r in [0, rows - 1]:
            if input_grid[r, c] == WHITE and not visited_white_from_border[r, c]:
                visited_white_from_border[r, c] = True
                queue.append((r, c))

    # Perform BFS to find all white pixels connected to the border white pixels
    while queue:
        r, c = queue.popleft()

        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white and not yet visited
                if input_grid[nr, nc] == WHITE and not visited_white_from_border[nr, nc]:
                    visited_white_from_border[nr, nc] = True
                    queue.append((nr, nc))

    # --- Step 3: Fill 'interior' white pixels ---

    # Iterate through the grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white in the original grid AND was NOT visited by the border BFS,
            # it's an 'interior' white pixel.
            if input_grid[r, c] == WHITE and not visited_white_from_border[r, c]:
                # Change its color to azure in the output grid
                output_grid[r, c] = AZURE

    # --- Step 4: Return the result ---
    return output_grid
```