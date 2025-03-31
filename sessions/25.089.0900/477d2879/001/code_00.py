import numpy as np
from collections import deque

def _find_reachable_pixels(grid):
    """
    Finds pixels reachable from the border without crossing blue (1) pixels.
    Uses Breadth-First Search (BFS).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: A boolean mask where True indicates a reachable pixel.
    """
    rows, cols = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add border cells that are not blue (1) to the queue
    for r in range(rows):
        if grid[r, 0] != 1:
            queue.append((r, 0))
            reachable_mask[r, 0] = True
        if grid[r, cols - 1] != 1:
            queue.append((r, cols - 1))
            reachable_mask[r, cols - 1] = True
    for c in range(1, cols - 1):
        if grid[0, c] != 1:
            queue.append((0, c))
            reachable_mask[0, c] = True
        if grid[rows - 1, c] != 1:
            queue.append((rows - 1, c))
            reachable_mask[rows - 1, c] = True

    # Perform BFS
    while queue:
        r, c = queue.popleft()

        # Check neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if not already visited, and if not blue
            if 0 <= nr < rows and 0 <= nc < cols and \
               not reachable_mask[nr, nc] and grid[nr, nc] != 1:
                reachable_mask[nr, nc] = True
                queue.append((nr, nc))

    return reachable_mask

def _manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Identify regions: 'background' (reachable from border without crossing blue),
       'containers' (blue pixels), and 'enclosed' (unreachable non-blue pixels).
    2. Identify 'seed' pixels: non-white, non-blue pixels in the background.
    3. Fill background white pixels: Each white background pixel takes the color
       of the nearest seed pixel (Manhattan distance, tie-breaking by row then column).
    4. Transform containers and enclosed areas:
        a. Find all 'internal colors' (non-white, non-blue colors in the enclosed area).
        b. Determine 'wall_color' for blue pixels: Red (2) if Red (2) is an internal color, else Azure (8).
        c. Determine 'fill_color' for enclosed white pixels: Green (3) if Green (3) is internal,
           else Magenta (6) if Magenta (6) is internal, else Azure (8).
        d. Update blue pixels to 'wall_color'.
        e. Update enclosed white pixels to 'fill_color'.
        f. Other pixels (seeds, internal colors) keep their original color.
    """
    
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid) # Initialize output grid as a copy

    # 1. Identify Regions using reachability
    reachable_mask = _find_reachable_pixels(input_grid)
    enclosed_mask = ~reachable_mask & (input_grid != 1)

    # 2. Identify Seeds
    seeds = []
    for r in range(rows):
        for c in range(cols):
            if reachable_mask[r, c] and input_grid[r, c] != 0 and input_grid[r, c] != 1:
                seeds.append({'pos': (r, c), 'color': input_grid[r, c]})

    # 3. Fill Background White Pixels (Voronoi Fill)
    if seeds: # Only fill if there are seeds
        for r in range(rows):
            for c in range(cols):
                if reachable_mask[r, c] and input_grid[r, c] == 0:
                    min_dist = float('inf')
                    nearest_seeds = []
                    for seed in seeds:
                        dist = _manhattan_distance((r, c), seed['pos'])
                        if dist < min_dist:
                            min_dist = dist
                            nearest_seeds = [seed]
                        elif dist == min_dist:
                            nearest_seeds.append(seed)

                    # Tie-breaking: lowest row, then lowest column
                    best_seed = min(nearest_seeds, key=lambda s: (s['pos'][0], s['pos'][1]))
                    output_grid[r, c] = best_seed['color']

    # 4a. Find all internal colors
    internal_colors = set()
    enclosed_white_pixels = []
    blue_pixels = []

    for r in range(rows):
        for c in range(cols):
            if enclosed_mask[r, c]:
                if input_grid[r,c] != 0: # non-white enclosed are internal colors
                   internal_colors.add(input_grid[r, c])
                else: # white enclosed
                    enclosed_white_pixels.append((r,c))
            elif input_grid[r, c] == 1: # Container pixel
                blue_pixels.append((r,c))

    # 4b. Determine wall_color
    wall_color = 8 # Default Azure
    if 2 in internal_colors: # If Red is present
        wall_color = 2

    # 4c. Determine fill_color
    fill_color = 8 # Default Azure
    if 3 in internal_colors:
        fill_color = 3
    elif 6 in internal_colors:
        fill_color = 6
    elif 8 in internal_colors:
         # If only 8 is present among 3,6,8, fill is 8 (already default)
         pass 
    # If none of 3, 6, 8 are present, but other internal colors (like 2) might be, 
    # the examples suggest 8 is still the fill color (e.g., train_1).
    # If there are no internal colors at all, what should the fill be?
    # Examples imply there *are* internal colors if there's enclosed space.
    # If there happens to be enclosed white space but NO internal colors (unlikely based on examples)
    # let's default to Azure(8) as per the priority logic.


    # 4d. Update blue pixels
    for r, c in blue_pixels:
        output_grid[r, c] = wall_color

    # 4e. Update enclosed white pixels
    for r, c in enclosed_white_pixels:
        output_grid[r, c] = fill_color

    # 4f. Other pixels (seeds, internal colors) retain their original color (already handled by copying)

    return output_grid.tolist() # Return as list of lists