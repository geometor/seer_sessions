"""
Perform a flood fill operation starting from all blue (1) pixels in the input grid.
The fill color is blue (1) and it expands into adjacent white (0) pixels.
The fill stops at the grid boundaries or any non-white (0) pixels.
All original non-white pixels retain their color and position.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies a flood fill operation starting from blue pixels (1).

    Args:
        input_grid (list of lists): The input grid representing pixel colors.

    Returns:
        list of lists: The transformed grid with white areas adjacent to blue pixels
                       filled with blue, bounded by non-white pixels or grid edges.
    """
    # Convert input to numpy array for easier indexing and manipulation
    np_input_grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(np_input_grid)
    height, width = output_grid.shape

    # Find initial starting points for the flood fill (blue pixels)
    start_points = np.argwhere(np_input_grid == 1)

    # Initialize queue for BFS flood fill and a set to track visited cells
    queue = deque()
    visited = set()

    # Add initial blue points to the queue and visited set
    # Note: We start filling *from* these points into adjacent white cells.
    # The blue points themselves are already blue. We add them to visited
    # to ensure we don't try to process them as fill targets.
    for r, c in start_points:
        # We don't actually need to add the blue pixels themselves to the queue,
        # but we need to consider their *neighbors* as potential starting points
        # for the fill into white areas.
        visited.add((r, c)) # Mark the blue pixel itself as 'visited' conceptually

        # Check neighbors of the initial blue pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) and not already visited
                if output_grid[nr, nc] == 0 and (nr, nc) not in visited:
                    # This white neighbor is a starting point for the actual fill
                    output_grid[nr, nc] = 1 # Fill it blue
                    visited.add((nr, nc))
                    queue.append((nr, nc))


    # Perform Breadth-First Search (BFS) flood fill
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white (0) and not already visited
                if output_grid[nr, nc] == 0 and (nr, nc) not in visited:
                    # Change color to blue (1)
                    output_grid[nr, nc] = 1
                    # Mark as visited
                    visited.add((nr, nc))
                    # Add to queue for further exploration
                    queue.append((nr, nc))

    # Convert the result back to a list of lists
    return output_grid.tolist()