import numpy as np
import collections

def transform(input_grid):
    """
    Transforms the input grid based on identifying regions enclosed by green (3) pixels.
    1. Initialize the output grid as an exact copy of the input grid.
    2. Identify all pixels in the input grid that are *not* green (3).
    3. Perform a flood fill (BFS) starting from all non-green pixels located on the border/edge of the grid. This fill represents the "outside" area.
    4. The flood fill can only spread to adjacent (up, down, left, right) pixels that are also *not* green (3) in the original input grid. Keep track of all visited pixels during this "outside" fill.
    5. After the "outside" fill is complete, iterate through all pixels in the grid.
    6. Any pixel that was *not* green (3) in the original input grid AND was *not* visited by the "outside" fill is considered to be part of an "enclosed" region.
    7. Change the color of all these identified "enclosed" pixels to azure (8) in the output grid.
    8. The final output grid contains the original green (3) pixels, the newly colored azure (8) enclosed regions, and the original non-green pixels that were part of the "outside" region.
    """

    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    boundary_color = 3
    fill_color = 8

    # Keep track of visited pixels during the "outside" fill
    visited = np.zeros_like(input_np, dtype=bool)
    q = collections.deque()

    # Initialize the queue with non-boundary pixels on the border
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on the border
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                # Check if it's not a boundary color and hasn't been visited
                if input_np[r, c] != boundary_color and not visited[r, c]:
                    visited[r, c] = True
                    q.append((r, c))

    # Perform BFS for the "outside" fill
    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is not a boundary and not visited
                if input_np[nr, nc] != boundary_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # Fill the enclosed regions (not green and not visited by outside fill)
    for r in range(height):
        for c in range(width):
            # If the pixel is not a boundary and was not reached by the outside fill
            if input_np[r, c] != boundary_color and not visited[r, c]:
                # It's an enclosed pixel, fill it with the target color
                output_np[r, c] = fill_color

    # Convert the result back to a list of lists
    return output_np.tolist()