import numpy as np
from collections import deque

"""
The transformation rule involves a constrained flood fill operation originating from white pixels adjacent to gray pixels.

1.  **Identify Seeds and Boundaries:**
    *   Red pixels (2) and gray pixels (5) act as strict boundaries for the fill.
    *   White pixels (0) immediately adjacent (cardinally) to any gray pixel (5) are the starting points (seeds) for the fill.

2.  **Perform Constrained Fill (BFS):**
    *   Initialize the output grid as a copy of the input grid.
    *   Create a queue for the Breadth-First Search (BFS) and a set to track visited pixels.
    *   Find all gray pixels (5) in the input grid.
    *   For each gray pixel, check its cardinal neighbors (up, down, left, right).
    *   If a neighbor is within bounds, is white (0), and hasn't been visited yet:
        *   Change its color to yellow (4) in the output grid.
        *   Add its coordinates to the BFS queue.
        *   Add its coordinates to the visited set.
    *   Add all red (2) and gray (5) pixel coordinates to the visited set initially, as they are boundaries and cannot be filled or passed through.
    *   While the BFS queue is not empty:
        *   Dequeue a pixel coordinate `(r, c)`.
        *   Explore its cardinal neighbors `(nr, nc)`.
        *   For each neighbor:
            *   Check if it's within grid bounds.
            *   Check if it hasn't been visited.
            *   If both are true:
                *   Add `(nr, nc)` to the visited set.
                *   If the pixel at `(nr, nc)` in the *input* grid is white (0):
                    *   Change its color to yellow (4) in the output grid.
                    *   Enqueue `(nr, nc)`.

3.  **Final Output:**
    *   The output grid contains the original red and gray pixels, the original white pixels untouched by the fill remain white, and the white pixels reachable from the seeds (within the boundaries) are changed to yellow.
"""

def transform(input_grid):
    """
    Applies a bounded flood fill starting from white neighbors of gray pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Define colors
    background_color = 0 # white (fillable)
    boundary_color_1 = 2   # red (barrier)
    boundary_color_2 = 5 # gray (barrier and seed adjacent)
    fill_color = 4       # yellow (fill result)

    queue = deque()
    visited = set()

    # Initialize visited set with boundary pixels (red and gray)
    gray_coords = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] == boundary_color_1 or grid[r, c] == boundary_color_2:
                visited.add((r, c))
                if grid[r, c] == boundary_color_2:
                    gray_coords.append((r, c))

    # Find initial seed pixels (white neighbors of gray) and add them to the queue
    for r_gray, c_gray in gray_coords:
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r_gray + dr, c_gray + dc

            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white and not already visited/queued
                if grid[nr, nc] == background_color and (nr, nc) not in visited:
                    output_grid[nr, nc] = fill_color
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    # Perform flood fill using BFS from the identified seed pixels
    while queue:
        r, c = queue.popleft()

        # Explore cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds and not visited
            if 0 <= nr < height and 0 <= nc < width and (nr, nc) not in visited:
                # Add to visited regardless of color to prevent re-checking
                visited.add((nr, nc))
                # If it's a white pixel, fill it and add to queue
                if grid[nr, nc] == background_color:
                    output_grid[nr, nc] = fill_color
                    queue.append((nr, nc))

    # Convert the result back to a list of lists format
    return output_grid.tolist()