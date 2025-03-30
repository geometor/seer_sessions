```python
"""
Fill connected white (0) areas starting from existing blue (1) pixels using an 8-connected flood fill.
Non-white pixels act as boundaries and remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Performs an 8-connected flood fill starting from blue (1) pixels,
    filling adjacent white (0) pixels with blue (1).

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Initialize a queue for the Breadth-First Search (BFS) flood fill
    queue = deque()

    # Find all initial blue pixels and add them to the queue
    # These are the starting points for the flood fill
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 1:  # Found a blue pixel
                queue.append((r, c))
                # Note: We don't change the color here yet, as it's already blue.
                # The important part is adding it as a source for spreading.

    # Define the 8 directions for neighbors (horizontal, vertical, diagonal)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Perform the BFS flood fill
    while queue:
        # Get the current pixel coordinates from the front of the queue
        r, c = queue.popleft()

        # Explore the 8 neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within the grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor pixel in the *output_grid* is white (0)
                # We check the output_grid because a neighbor might have been
                # filled in a previous step of the BFS.
                if output_grid[nr, nc] == 0:
                    # Change the white pixel to blue
                    output_grid[nr, nc] = 1
                    # Add the newly filled neighbor to the queue to process its neighbors
                    queue.append((nr, nc))

    # Return the modified grid
    return output_grid
```