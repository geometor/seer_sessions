"""
Transforms the input grid by filling enclosed white regions within yellow shapes with yellow, where enclosure is defined by 4-way connectivity.

The transformation identifies white pixels (color 0) that are connected to the boundary of the grid
using 4-way connectivity (horizontal and vertical only). Any white pixel that is not
connected to the boundary is considered enclosed by the yellow shape (color 4) or other enclosed
white regions. These enclosed white pixels are then changed to yellow (color 4).

If there are no enclosed white regions, the output grid will be identical to the input grid.
"""

import numpy as np
from collections import deque

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Create a boolean grid to keep track of visited white pixels during flood fill
    # These visited pixels represent the "exterior" white region connected to the boundary
    visited_exterior_white = np.zeros_like(input_grid, dtype=bool)

    # Use a queue for Breadth-First Search (BFS) to find all white pixels connected to the boundary
    q = deque()

    # Identify initial white pixels on the boundary and add them to the queue
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is on the boundary
            is_boundary = (r == 0 or r == rows - 1 or c == 0 or c == cols - 1)
            # If it's a white pixel (0) on the boundary and hasn't been visited yet
            if is_boundary and input_grid[r, c] == 0 and not visited_exterior_white[r, c]:
                q.append((r, c))
                visited_exterior_white[r, c] = True # Mark as visited

    # Perform BFS flood fill from boundary white pixels using 4-way connectivity
    while q:
        r, c = q.popleft()

        # Explore 4 neighbours (horizontal, vertical)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbour is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbour is white (0) and hasn't been visited
                if input_grid[nr, nc] == 0 and not visited_exterior_white[nr, nc]:
                    visited_exterior_white[nr, nc] = True # Mark as visited
                    q.append((nr, nc)) # Add to queue for further exploration

    # Iterate through all pixels in the grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is white (0) but was *not* visited by the BFS
            # (meaning it's not connected to the boundary via 4-way paths), it's an enclosed white pixel
            if input_grid[r, c] == 0 and not visited_exterior_white[r, c]:
                # Change its color to yellow (4) in the output grid
                output_grid[r, c] = 4

    # Return the modified grid
    return output_grid