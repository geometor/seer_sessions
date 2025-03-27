import numpy as np
from collections import deque

"""
Identifies white (0) regions connected to the left edge (column 0) but not connected to any other boundary edge (top, bottom, right). 
These identified regions are then filled with red (2). 
Blue (1) pixels act as barriers, blocking connectivity. 
Connectivity is defined by orthogonal adjacency (up, down, left, right).
"""

def _flood_fill(grid, start_coords, traversal_color):
    """
    Performs a flood fill to find all reachable cells of traversal_color.

    Args:
        grid (np.ndarray): The input grid.
        start_coords (list[tuple[int, int]]): List of starting coordinates (r, c).
        traversal_color (int): The color of pixels to traverse through.

    Returns:
        set[tuple[int, int]]: A set of coordinates (r, c) reachable from start_coords
                               by traversing pixels of traversal_color.
    """
    height, width = grid.shape
    reachable = set()
    visited = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Initialize queue with valid starting coordinates that match traversal_color
    for r, c in start_coords:
        if 0 <= r < height and 0 <= c < width and grid[r, c] == traversal_color and not visited[r, c]:
            queue.append((r, c))
            visited[r, c] = True
            reachable.add((r, c))

    # Perform BFS
    while queue:
        r, c = queue.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is the traversal color and hasn't been visited
                if grid[nr, nc] == traversal_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    reachable.add((nr, nc))
                    queue.append((nr, nc))
    return reachable

def transform(input_grid):
    """
    Transforms the input grid by filling specific white regions red.

    A white region is filled red if it's reachable from the left edge via
    other white pixels, but not reachable from any boundary (top, bottom,
    left, right) via other white pixels. Blue pixels act as barriers.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Constants for colors
    white = 0
    # blue = 1 # Blue acts as implicit barrier by not being white
    red = 2

    # 1. Identify Left-Reachable White Pixels
    # Find starting white pixels on the left edge
    left_edge_starts = []
    for r in range(height):
        if grid[r, 0] == white:
            left_edge_starts.append((r, 0))
    
    # Perform flood fill from the left edge through white pixels
    left_reachable = _flood_fill(grid, left_edge_starts, white)

    # 2. Identify Boundary-Reachable White Pixels
    # Find starting white pixels on all boundaries
    boundary_starts_set = set()
    # Top boundary
    for c in range(width):
        if grid[0, c] == white:
            boundary_starts_set.add((0, c))
    # Bottom boundary
    for c in range(width):
        if grid[height - 1, c] == white:
            boundary_starts_set.add((height - 1, c))
    # Left boundary
    for r in range(height):
        if grid[r, 0] == white:
            boundary_starts_set.add((r, 0))
    # Right boundary
    for r in range(height):
        if grid[r, width - 1] == white:
            boundary_starts_set.add((r, width - 1))
            
    boundary_starts = list(boundary_starts_set)

    # Perform flood fill from all boundary points through white pixels
    boundary_reachable = _flood_fill(grid, boundary_starts, white)

    # 3. Determine Target Pixels for Filling
    # Target pixels are those reachable from the left but not from the general boundary
    target_pixels = left_reachable - boundary_reachable

    # 4. Construct the Output Grid
    # Initialize output_grid as a copy of the input grid
    output_grid = grid.copy()

    # Change the color of target pixels to red
    for r, c in target_pixels:
        output_grid[r, c] = red

    # Convert back to list of lists before returning
    return output_grid.tolist()