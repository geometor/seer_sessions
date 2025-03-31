import numpy as np
from collections import deque

def transform(input_grid):
    """
    Identify the region enclosed by the gray (5) boundary using a flood fill
    from the border white (0) pixels. The 'inside' white pixels are those not
    reached by this flood fill. Fill these 'inside' white pixels with azure (8).

    Also, identify all 'outside' white pixels (those reached by the flood fill).
    Find the set of rows and columns occupied by either the gray boundary pixels
    or the 'inside' white pixels (which will be filled with azure).
    Fill any 'outside' white pixel with azure (8) if its row index is present
    in the set of occupied rows OR its column index is present in the set of
    occupied columns.

    Gray pixels remain unchanged.
    """

    # Define colors
    WHITE = 0
    GRAY = 5
    AZURE = 8

    # Get grid dimensions
    height, width = input_grid.shape

    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Keep track of visited white pixels reachable from the border (outside region)
    visited_outside = np.zeros_like(input_grid, dtype=bool)

    # Initialize queue for Breadth-First Search (BFS) flood fill
    queue = deque()

    # Add all white border pixels to the queue and mark as visited
    for r in range(height):
        if input_grid[r, 0] == WHITE and not visited_outside[r, 0]:
            queue.append((r, 0))
            visited_outside[r, 0] = True
        if width > 1 and input_grid[r, width - 1] == WHITE and not visited_outside[r, width - 1]:
            queue.append((r, width - 1))
            visited_outside[r, width - 1] = True

    for c in range(width):
        # Avoid double-adding corners already added by row loop
        if input_grid[0, c] == WHITE and not visited_outside[0, c]:
             queue.append((0, c))
             visited_outside[0, c] = True
        if height > 1 and input_grid[height - 1, c] == WHITE and not visited_outside[height - 1, c]:
             queue.append((height - 1, c))
             visited_outside[height - 1, c] = True

    # Perform BFS flood fill from border white pixels
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right) - 4-connectivity is sufficient for region filling
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is white and not visited
                if input_grid[nr, nc] == WHITE and not visited_outside[nr, nc]:
                    visited_outside[nr, nc] = True
                    queue.append((nr, nc))

    # Identify coordinates of internal white pixels and gray boundary pixels
    internal_white_coords = []
    boundary_coords = []
    occupied_rows = set()
    occupied_cols = set()

    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == GRAY:
                boundary_coords.append((r, c))
                occupied_rows.add(r)
                occupied_cols.add(c)
            elif input_grid[r, c] == WHITE and not visited_outside[r, c]:
                internal_white_coords.append((r, c))
                occupied_rows.add(r)
                occupied_cols.add(c)

    # Fill internal white pixels
    for r, c in internal_white_coords:
        output_grid[r, c] = AZURE

    # Fill external white pixels that share a row or column with the boundary or internal area
    for r in range(height):
        for c in range(width):
            # Check if it's an external white pixel
            if input_grid[r, c] == WHITE and visited_outside[r, c]:
                # Check if it shares a row or column with the occupied region
                if r in occupied_rows or c in occupied_cols:
                    output_grid[r, c] = AZURE

    return output_grid