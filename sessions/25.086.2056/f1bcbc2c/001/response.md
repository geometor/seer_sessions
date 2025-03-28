```python
"""
Identifies regions enclosed by orange (7) pixels in the input grid and fills
these regions (originally white(0) or maroon(9)) with azure (8).
Non-orange pixels reachable from the grid border without crossing orange pixels
remain unchanged. Orange pixels also remain unchanged.
"""

import numpy as np
from collections import deque

# Define color constants for clarity
BG_WHITE = 0
BOUNDARY_ORANGE = 7
FILL_AZURE = 8
SPECIAL_MAROON = 9 # Treated like BG_WHITE for connectivity and fill eligibility

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies a flood-fill like transformation to the input grid.

    It identifies all areas of non-orange pixels (white or maroon) that are
    completely enclosed by orange pixels (i.e., cannot be reached from the
    grid border without crossing an orange pixel). These enclosed areas are
    then filled with the azure color.

    Args:
        input_grid: A 2D numpy array representing the input grid with integer
                    color values (0-9).

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    rows, cols = input_grid.shape
    # Initialize output_grid as a copy of the input. We will modify this.
    output_grid = np.copy(input_grid)
    # Initialize a grid to keep track of visited non-boundary pixels reachable from the border.
    visited = np.zeros_like(input_grid, dtype=bool)
    # Initialize a queue for the Breadth-First Search (BFS).
    queue = deque()

    # Helper function for getting valid 4-directional neighbors within grid bounds.
    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-directional neighbors
            nr, nc = r + dr, c + dc
            # Check if the neighbor coordinates are within the grid bounds.
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    # --- Step 1: Seed the BFS queue with non-boundary pixels on the border ---
    # Iterate through all border positions (top/bottom rows, left/right columns).
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is on any border.
            is_border = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
            if not is_border:
                continue # Skip non-border pixels in this initial seeding step.

            # If it's a border pixel, check if it's NOT a boundary color (orange)
            # and if it hasn't been visited yet (important for corners).
            if input_grid[r, c] != BOUNDARY_ORANGE and not visited[r, c]:
                visited[r, c] = True # Mark as visited.
                queue.append((r, c)) # Add to the queue to start BFS from here.

    # --- Step 2: Perform BFS to mark all non-boundary pixels reachable from the border ---
    while queue:
        r, c = queue.popleft() # Get the next pixel from the queue.

        # Explore its valid neighbors.
        for nr, nc in get_neighbors(r, c):
            # Check if the neighbor is NOT a boundary color AND hasn't been visited yet.
            if input_grid[nr, nc] != BOUNDARY_ORANGE and not visited[nr, nc]:
                visited[nr, nc] = True # Mark the reachable neighbor as visited.
                queue.append((nr, nc)) # Add it to the queue to explore from it later.

    # --- Step 3: Fill the enclosed areas in the output grid ---
    # Iterate through all pixels in the grid (including interior pixels).
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is NOT a boundary color (i.e., it's white or maroon)
            # AND it was NOT visited during the BFS starting from the border.
            if input_grid[r, c] != BOUNDARY_ORANGE and not visited[r, c]:
                # This pixel belongs to an enclosed region.
                # Change its color to the fill color (azure) in the output grid.
                output_grid[r, c] = FILL_AZURE

    # --- Step 4: Return the resulting grid ---
    return output_grid
```