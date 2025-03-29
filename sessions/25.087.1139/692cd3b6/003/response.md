```python
import numpy as np
from collections import deque

"""
Performs a flood fill operation on a grid, starting conceptually from gray pixels (5).

The transformation rule is as follows:
1. Initialize the output grid as a copy of the input grid.
2. Identify all gray (5) pixels.
3. Find all white (0) pixels that are cardinally adjacent to any gray pixel. These are the starting points (seeds) for the fill.
4. Perform a Breadth-First Search (BFS) starting from these seed pixels.
5. During the BFS, change reachable white (0) pixels to yellow (4).
6. The fill propagates cardinally (up, down, left, right).
7. Red (2) pixels act as impassable boundaries; the fill cannot enter or cross them.
8. Gray (5) pixels also act as barriers (in addition to being start points) and remain unchanged.
9. Only white pixels connected to the initial seed pixels (without crossing red or gray boundaries) are filled yellow.
10. All original red (2) and gray (5) pixels remain unchanged in the output. White pixels not reached by the fill also remain unchanged.
"""

def transform(input_grid):
    """
    Applies a bounded flood fill starting from neighbors of gray pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Define colors
    background_color = 0 # white (fillable)
    boundary_color = 2   # red (barrier)
    start_pixel_color = 5 # gray (origin point, also barrier)
    fill_color = 4       # yellow (fill result)

    # Initialize queue for Breadth-First Search (BFS)
    queue = deque()
    # Keep track of visited coordinates to avoid redundant processing and loops
    visited = set()

    # Find all gray and red pixels, mark them as visited initially
    # as they are barriers and should not be filled or added to the queue.
    gray_coords = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] == start_pixel_color:
                visited.add((r, c))
                gray_coords.append((r,c))
            elif grid[r, c] == boundary_color:
                visited.add((r, c))

    # Find initial white seed pixels adjacent to any gray pixel
    for start_row, start_col in gray_coords:
        # Check cardinal neighbors of each gray pixel
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = start_row + dr, start_col + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is white and hasn't been visited/queued yet
                if grid[nr, nc] == background_color and (nr, nc) not in visited:
                    # This is a seed pixel: change its color in the output
                    output_grid[nr, nc] = fill_color
                    # Mark as visited
                    visited.add((nr, nc))
                    # Add to queue to start BFS from here
                    queue.append((nr, nc))

    # Perform flood fill using BFS from the identified seed pixels
    while queue:
        r, c = queue.popleft()

        # Explore cardinal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor hasn't been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is the background color (fillable) in the original grid
                    if grid[nr, nc] == background_color:
                        # Change color in the output grid
                        output_grid[nr, nc] = fill_color
                        # Mark as visited
                        visited.add((nr, nc))
                        # Add to queue for further exploration
                        queue.append((nr, nc))
                    else:
                         # If it's not background (e.g., red or gray), mark it visited
                         # so we don't try to process it again from another path.
                         # We already marked red/gray pixels at the start, but this catches
                         # potential other non-background colors if they existed, and reinforces boundary marking.
                         visited.add((nr, nc))

    # Convert the result back to a list of lists format
    return output_grid.tolist()
```