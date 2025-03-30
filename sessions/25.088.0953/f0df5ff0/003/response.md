```python
"""
Performs an 8-connected flood fill starting from blue (1) pixels,
filling adjacent white (0) pixels with blue (1). Pixels with colors
other than white (0) or blue (1) act as impassable boundaries for the fill.
Original blue pixels and boundary pixels remain unchanged.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills connected white areas (color 0) with blue (color 1) starting 
    from existing blue pixels, using 8-way connectivity. Non-white, non-blue 
    pixels act as boundaries.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    # Create a copy of the input grid to modify. This ensures non-white, 
    # non-blue pixels are preserved and acts as the canvas for filling.
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Initialize a queue for the Breadth-First Search (BFS) flood fill.
    queue = deque()

    # Find all initial blue pixels (color 1) in the input grid.
    # These are the starting points for the flood fill.
    # Add their coordinates to the queue. We don't need to change their color
    # as they are already blue in the output_grid copy.
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 1:  # Found an initial blue pixel
                queue.append((r, c))
                # No need to mark as visited explicitly here, as the check later 
                # `output_grid[nr, nc] == 0` prevents re-adding blue cells.

    # Define the 8 directions for neighbors (horizontal, vertical, diagonal).
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Perform the BFS flood fill.
    while queue:
        # Get the current pixel coordinates from the front of the queue.
        r, c = queue.popleft()

        # Explore the 8 neighbors of the current pixel.
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check 1: Is the neighbor within the grid boundaries?
            if 0 <= nr < height and 0 <= nc < width:
                # Check 2: Is the neighbor pixel white (0) in the output_grid?
                # This is the crucial check:
                # - Ensures we only fill white pixels.
                # - Prevents filling pixels that are already blue (initial or filled).
                # - Prevents filling pixels with boundary colors (2-9).
                # - Prevents re-adding already processed/filled pixels to the queue.
                if output_grid[nr, nc] == 0:
                    # If the neighbor is white, change it to blue (1).
                    output_grid[nr, nc] = 1
                    # Add the newly filled neighbor's coordinates to the queue 
                    # so its neighbors can be explored later.
                    queue.append((nr, nc))

    # Return the modified grid after the flood fill is complete.
    return output_grid
```