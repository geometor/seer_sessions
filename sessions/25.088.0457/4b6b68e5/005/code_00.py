import numpy as np
from collections import deque, Counter

"""
Identifies contiguous shapes of a single non-white color in the input grid.
For each shape, determines if it is "closed" by checking if it encloses an interior region 
(pixels not reachable from the grid boundary without crossing the shape).

If a shape is closed:
1. Its boundary pixels are copied to the output grid (initially all white) using the boundary color.
2. The interior region is identified.
3. "Marker" pixels (non-white, non-boundary color) within the interior region are collected from the input grid.
4. The number of *distinct* marker colors is counted.
5. If there are two or more distinct marker colors:
   a. The frequency of each marker color is counted.
   b. The most frequent marker color is determined.
   c. If there is a tie in frequency, the marker color with the *lowest* numerical value is chosen. This becomes the "fill color".
   d. All pixels within the interior region are set to the fill color in the output grid.
6. If a closed shape has fewer than two distinct marker colors in its interior, the interior remains white (0) in the output grid, and only the boundary is drawn.

Pixels belonging to shapes that are not closed, or pixels not part of any closed shape's boundary or filled interior, remain white (0) in the final output grid.
"""

def find_shapes_and_boundaries(grid):
    """
    Finds all distinct contiguous shapes of non-white colors.
    Returns a list of tuples, where each tuple contains:
    (set of boundary pixel coordinates, boundary_color)
    """
    H, W = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []

    for r in range(H):
        for c in range(W):
            # If it's a non-white pixel and not yet visited
            if grid[r, c] != 0 and not visited[r, c]:
                boundary_color = grid[r, c]
                boundary_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                boundary_pixels.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < H and 0 <= nc < W and \
                           not visited[nr, nc] and \
                           grid[nr, nc] == boundary_color:
                            visited[nr, nc] = True
                            boundary_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                # Ensure shape has pixels before adding
                if boundary_pixels: 
                     shapes.append((boundary_pixels, boundary_color))
    return shapes

def find_reachable(grid_shape, starts, impassable_pixels):
    """
    Finds all pixels reachable from start points without crossing impassable pixels using BFS.
    grid_shape is a tuple (H, W).
    starts is a list or set of (r, c) tuples.
    impassable_pixels is a set of (r, c) tuples.
    Returns a set of reachable (r, c) tuples.
    """
    H, W = grid_shape
    # Filter out start points that are themselves impassable
    q = deque(p for p in starts if 0 <= p[0] < H and 0 <= p[1] < W and p not in impassable_pixels)
    reachable = set(q) # Initialize reachable with valid, non-impassable start points
    
    # Optimization: Keep track of visited to avoid redundant checks, initialize with reachable
    visited = np.zeros(grid_shape, dtype=bool)
    for r, c in reachable:
        visited[r,c] = True

    while q:
        r, c = q.popleft()

        # Explore neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check bounds, visited status, and impassable status
            if 0 <= nr < H and 0 <= nc < W and \
               not visited[nr, nc] and \
               (nr, nc) not in impassable_pixels:
                visited[nr, nc] = True
                reachable.add((nr, nc))
                q.append((nr, nc))
    return reachable


def get_interior_region(grid_shape, boundary_pixels):
    """
    Determines the interior region enclosed by a set of boundary pixels.
    Returns the set of interior pixels if the boundary forms a closed shape,
    otherwise returns an empty set.
    """
    H, W = grid_shape
    all_pixels = set((r, c) for r in range(H) for c in range(W))
    potential_interior_exterior = all_pixels - boundary_pixels

    # If no pixels other than the boundary exist, no interior is possible
    if not potential_interior_exterior:
        return set()

    # Define starting points for exterior flood fill: all edge points *not* on the boundary
    edge_starts = set()
    for r in range(H):
        if (r, 0) not in boundary_pixels: edge_starts.add((r, 0))
        if (r, W - 1) not in boundary_pixels: edge_starts.add((r, W - 1))
    for c in range(1, W - 1): # Avoid adding corners twice
        if (0, c) not in boundary_pixels: edge_starts.add((0, c))
        if (H - 1, c) not in boundary_pixels: edge_starts.add((H - 1, c))

    # If there are no valid starting points for the exterior (e.g., boundary touches all edges),
    # then all non-boundary points *could* be interior. We still need the reachability check.
    # But if edge_starts is empty AND potential_interior_exterior is not empty, it implies
    # the boundary perfectly frames the grid, making everything inside potential interior.
    # The flood fill handles this correctly. If edge_starts is empty because ALL edge points
    # ARE on the boundary, find_reachable will return an empty set for exterior_pixels
    # (as no starting points are valid), which is correct.

    # Find all pixels reachable from the edges without crossing the boundary
    exterior_pixels = find_reachable(grid_shape, edge_starts, boundary_pixels)

    # The interior is whatever potential pixels are left after removing the exterior
    interior_pixels = potential_interior_exterior - exterior_pixels

    # If interior_pixels is not empty, the shape is considered closed w.r.t the grid boundary
    # This also implicitly handles cases where a shape might enclose another shape entirely.
    # The outer shape's interior calculation will correctly identify the inner area.
    # The inner shape will be processed separately.
    return interior_pixels


def transform(input_grid):
    """
    Transforms the input grid based on closed shapes and internal marker diversity.
    """
    H, W = input_grid.shape
    # Initialize output grid with background color (white/0)
    output_grid = np.zeros_like(input_grid)

    # 1. Find all distinct shapes (boundaries) and their colors
    shapes = find_shapes_and_boundaries(input_grid)

    # 2. Process each shape found
    for boundary_pixels, boundary_color in shapes:

        # 3. Determine if the shape is closed and find its potential interior
        interior_region_pixels = get_interior_region((H, W), boundary_pixels)

        # 4. If the shape is closed (has an interior)
        if interior_region_pixels:
            # a. Copy the boundary pixels to the output grid
            for r, c in boundary_pixels:
                if 0 <= r < H and 0 <= c < W: # Bounds check for safety
                     output_grid[r, c] = boundary_color

            # b. Collect marker colors from the *input* grid within the interior region
            marker_colors = []
            for r, c in interior_region_pixels:
                if 0 <= r < H and 0 <= c < W: # Bounds check for safety
                    pixel_color = input_grid[r, c]
                    # A marker is non-white and not the boundary color
                    if pixel_color != 0 and pixel_color != boundary_color:
                        marker_colors.append(pixel_color)

            # c. Check the fill condition: at least two *distinct* marker colors
            distinct_marker_colors = set(marker_colors)
            
            fill_color = None # Initialize fill color
            if len(distinct_marker_colors) >= 2:
                # d. Condition met: Determine the fill color
                if marker_colors: # Should be true if distinct_marker_colors >= 2
                    color_counts = Counter(marker_colors)
                    # Find the maximum frequency
                    max_freq = 0
                    for color in color_counts:
                        max_freq = max(max_freq, color_counts[color])

                    # Find all colors with max frequency
                    candidate_colors = [color for color, count in color_counts.items() if count == max_freq]

                    # Tie-breaking: Choose the color with the *lowest* numerical value
                    fill_color = min(candidate_colors)

            # e. Fill the interior region in the output grid if a fill_color was determined
            if fill_color is not None:
                for r, c in interior_region_pixels:
                     if 0 <= r < H and 0 <= c < W: # Bounds check for safety
                        output_grid[r, c] = fill_color
            # Else (fill condition not met or no markers), the interior remains white (0)

    # 5. Unclosed shapes are ignored (never processed in step 4).
    # 6. Pixels not part of a closed boundary or a filled interior remain white.
    # 7. Return the completed output grid
    return output_grid