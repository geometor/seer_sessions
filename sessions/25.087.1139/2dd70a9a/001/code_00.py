import numpy as np
from collections import deque

"""
Identify all pixels belonging to the source object (green, 3), the target object (red, 2), and obstacles (azure, 8) in the input grid.
Find the shortest path(s) between any green pixel and any red pixel, moving only through white (0) pixels and avoiding azure (8) pixels (and other non-white pixels). Use 4-directional adjacency (up, down, left, right).
If a path exists, determine the minimum path length (number of white cells in the path + 1).
Identify all white (0) pixels that lie on any path of this minimum length between a green pixel and a red pixel.
Create the output grid by copying the input grid, then change the color of all identified shortest path white pixels to green (3).
If no path exists between green and red pixels, return the input grid unchanged.
"""

def find_pixels(grid, color):
    """Finds all pixels of a specific color."""
    rows, cols = grid.shape
    pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                pixels.append((r, c))
    return pixels

def bfs(grid, start_pixels, end_pixels_set, obstacle_color=8, traversable_color=0):
    """
    Performs a Breadth-First Search to find shortest paths.

    Args:
        grid: The input numpy array.
        start_pixels: A list of (row, col) tuples representing starting points.
        end_pixels_set: A set of (row, col) tuples representing target points.
        obstacle_color: The color code for obstacles.
        traversable_color: The color code for traversable cells.

    Returns:
        A tuple: (min_distance, distances_grid)
        min_distance: The shortest distance found to any end pixel, or -1 if unreachable.
        distances_grid: A grid of the same shape as input, storing the shortest distance
                         from any start_pixel to that cell, or -1 if unreachable.
    """
    rows, cols = grid.shape
    distances = np.full((rows, cols), -1, dtype=int)
    queue = deque()
    min_dist_to_target = -1

    # Initialize queue and distances for all start pixels
    for r, c in start_pixels:
        if 0 <= r < rows and 0 <= c < cols:
            # Starting pixels themselves are not part of the path length calculation if they are not traversable_color
            # But BFS starts conceptually *at* them. Let's assume distance 0 for them.
             distances[r, c] = 0
             queue.append(((r, c), 0)) # ((row, col), distance)

    # Initialize queue and distances for traversable cells adjacent to start pixels
    processed_starts = set(start_pixels) # Keep track of starts already added
    initial_queue_len = len(queue)
    for _ in range(initial_queue_len):
         (sr, sc), _ = queue.popleft() # Use the initial starts to find the first step
         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
             nr, nc = sr + dr, sc + dc
             if 0 <= nr < rows and 0 <= nc < cols:
                cell_val = grid[nr, nc]
                # Check if it's a traversable cell OR a target cell (targets can be occupied)
                is_traversable = (cell_val == traversable_color)
                is_target = (nr, nc) in end_pixels_set

                if (is_traversable or is_target) and distances[nr, nc] == -1:
                    distances[nr, nc] = 1 # First step onto a valid cell
                    queue.append(((nr, nc), 1))
                    processed_starts.add((nr, nc)) # Mark as visited to avoid re-adding

    # Perform BFS
    while queue:
        (r, c), dist = queue.popleft()

        # Check if this cell is a target
        if (r, c) in end_pixels_set:
            if min_dist_to_target == -1 or dist < min_dist_to_target:
                 min_dist_to_target = dist
            # Don't stop; continue BFS to find all cells reachable at potentially minimum distance

        # If we already exceeded the minimum distance found to a target,
        # we don't need to explore further from this path for finding *shortest* paths cells.
        # However, we need the full distance map for the backward pass verification.
        # Let's refine this later if needed for performance. Just continue BFS for now.

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and distances[nr, nc] == -1:
                cell_val = grid[nr, nc]
                is_traversable = (cell_val == traversable_color)
                is_target = (nr, nc) in end_pixels_set # Allow moving onto target cells

                if is_traversable or is_target:
                     distances[nr, nc] = dist + 1
                     queue.append(((nr, nc), dist + 1))

    return min_dist_to_target, distances


def transform(input_grid_list):
    """
    Transforms the input grid by finding the shortest path(s) between green (3)
    and red (2) pixels through white (0) pixels, avoiding azure (8) pixels,
    and coloring the white pixels on these paths green (3).
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify Key Components
    green_pixels = find_pixels(input_grid, 3)
    red_pixels = find_pixels(input_grid, 2)
    red_pixels_set = set(red_pixels)
    # Obstacles are implicitly handled by BFS (only allows traversal on white=0 or targets=2)
    # white_pixels = find_pixels(input_grid, 0) # Not explicitly needed upfront

    if not green_pixels or not red_pixels:
        return output_grid.tolist() # No start or end points, return original

    # 2. Forward BFS: Find shortest path distance from Green to Red
    # Start BFS from *adjacent* white/red cells to green cells, or directly from green cells if they are white/red?
    # The description implies the path is made of *white* cells connecting green to red.
    # Let's adjust BFS: start points are green, but the path cells counted are white.
    # Rerun BFS logic: Start search *from* green cells. Distance to first adjacent white/red cell is 1.
    # Let's stick to the standard BFS: starts are green pixels, targets are red pixels.
    # Path cost is moves through white pixels.

    min_dist_fwd, dist_from_green = bfs(input_grid, green_pixels, red_pixels_set, obstacle_color=8, traversable_color=0)

    # If no path exists
    if min_dist_fwd == -1:
        return output_grid.tolist()

    # 3. Backward BFS: Find shortest path distance from Red (reached at min_dist_fwd) to Green
    # Identify the red pixels that were reached at the minimum distance
    target_red_pixels_min_dist = [p for p in red_pixels if dist_from_green[p[0], p[1]] == min_dist_fwd]

    # Perform BFS starting from these specific red pixels
    # The target for this BFS is technically the green pixels, but we just need distances.
    # We are looking for white cells reachable from these specific red pixels.
    min_dist_bwd, dist_from_red = bfs(input_grid, target_red_pixels_min_dist, set(green_pixels), obstacle_color=8, traversable_color=0)


    # 4. Identify All Shortest Path Pixels (White cells only)
    # A white pixel (r, c) is on a shortest path if:
    # - It's reachable from a green start (dist_from_green[r, c] != -1)
    # - It's reachable from a red end (dist_from_red[r, c] != -1)
    # - The sum of distances equals the minimum total distance found (dist_from_green[r, c] + dist_from_red[r, c] == min_dist_fwd)
    # Note: The distances calculated by BFS count the number of steps/cells.
    # Example: Green -> White -> Red. Dist Green to White = 1. Dist Red to White = 1. Min Dist = 2. 1+1=2. Correct.
    # Example: Green -> White1 -> White2 -> Red. Dist G->W1=1, G->W2=2. Dist R->W1=2, R->W2=1. Min Dist = 3.
    # White1: dist_g=1, dist_r=2. Sum=3. Path cell.
    # White2: dist_g=2, dist_r=1. Sum=3. Path cell.

    path_color = 3 # Green
    for r in range(rows):
        for c in range(cols):
            # Check if it's a white pixel
            if input_grid[r, c] == 0:
                dist_g = dist_from_green[r, c]
                dist_r = dist_from_red[r, c]

                # Check if reachable from both ends and if the sum matches min_dist
                if dist_g != -1 and dist_r != -1 and (dist_g + dist_r == min_dist_fwd):
                    output_grid[r, c] = path_color

    return output_grid.tolist()