import numpy as np
from collections import deque, Counter

"""
Identifies contiguous shapes of a single non-white color in the input grid.
For each shape, determines if it is "closed" by checking if it encloses an interior region (pixels not reachable from the grid boundary without crossing the shape).
If a shape is closed:
  1. Its boundary pixels are copied to the output grid (initially all white).
  2. The interior region is identified.
  3. "Marker" pixels (non-white, non-boundary color) within the interior region are collected from the input grid.
  4. If markers exist, the most frequent marker color is determined (highest numerical value breaks ties). This becomes the "fill color".
  5. All pixels within the interior region (including originally white pixels or marker pixels) are set to the fill color in the output grid.
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
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < H and 0 <= nc < W and \
                           not visited[nr, nc] and \
                           grid[nr, nc] == boundary_color:
                            visited[nr, nc] = True
                            boundary_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                if boundary_pixels: # Should always be true if we start on non-white
                     shapes.append((boundary_pixels, boundary_color))
    return shapes

def find_reachable(grid_shape, starts, impassable_pixels):
    """
    Finds all pixels reachable from start points without crossing impassable pixels using BFS.
    grid_shape is a tuple (H, W).
    starts is a list or set of (r, c) tuples.
    impassable_pixels is a set of (r, c) tuples.
    """
    H, W = grid_shape
    q = deque(starts)
    reachable = set(starts)
    # Optimization: Filter out starts that are impassable
    q = deque(p for p in starts if p not in impassable_pixels)
    reachable = set(p for p in starts if p not in impassable_pixels)
    visited = np.zeros(grid_shape, dtype=bool)

    for r, c in reachable:
         if 0 <= r < H and 0 <= c < W: # Check bounds just in case start points were invalid
            visited[r,c] = True

    while q:
        r, c = q.popleft()

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

    if not potential_interior_exterior:
        return set() # No pixels other than boundary, cannot have interior

    # Define starting points for exterior flood fill (all edge points *not* on the boundary)
    edge_starts = set()
    for r in range(H):
        if (r, 0) not in boundary_pixels: edge_starts.add((r, 0))
        if (r, W - 1) not in boundary_pixels: edge_starts.add((r, W - 1))
    for c in range(1, W - 1): # Avoid adding corners twice
        if (0, c) not in boundary_pixels: edge_starts.add((0, c))
        if (H - 1, c) not in boundary_pixels: edge_starts.add((H - 1, c))

    # Find all pixels reachable from the edges without crossing the boundary
    exterior_pixels = find_reachable(grid_shape, edge_starts, boundary_pixels)

    # The interior is whatever is left that isn't boundary and isn't exterior
    interior_pixels = potential_interior_exterior - exterior_pixels

    # If interior_pixels is not empty, the shape is closed
    return interior_pixels


def transform(input_grid):
    """
    Transforms the input grid by finding closed shapes, identifying their interiors,
    determining a fill color based on the most frequent internal marker (if any),
    and filling the interior. Only closed shapes' boundaries and filled interiors
    are drawn onto an initially white output grid.
    """
    H, W = input_grid.shape
    # Initialize output grid with background color (white/0)
    output_grid = np.zeros_like(input_grid)

    # 1. Find all distinct shapes (boundaries) and their colors
    shapes = find_shapes_and_boundaries(input_grid)

    # 2. Process each shape
    for boundary_pixels, boundary_color in shapes:

        # 3a. Determine if the shape is closed and find its interior
        interior_region_pixels = get_interior_region((H, W), boundary_pixels)

        # 3b. If the shape is closed
        if interior_region_pixels:
            # i. Copy boundary pixels to output grid
            for r, c in boundary_pixels:
                output_grid[r, c] = boundary_color

            # ii. Identify interior region (already done)
            # iii. Collect marker colors from the *input* grid within the interior region
            marker_colors = []
            for r, c in interior_region_pixels:
                pixel_color = input_grid[r, c]
                # Marker is non-white and not the boundary color
                if pixel_color != 0 and pixel_color != boundary_color:
                    marker_colors.append(pixel_color)

            # iv. Determine fill color if markers exist
            fill_color = None
            if marker_colors:
                color_counts = Counter(marker_colors)
                max_freq = 0
                # Find the max frequency
                # Using .most_common() handles finding max frequency implicitly
                # It returns list of (element, count) sorted by count descending
                most_common_pairs = color_counts.most_common()
                if most_common_pairs:
                    max_freq = most_common_pairs[0][1]

                    # Find all colors with max frequency
                    candidate_colors = [color for color, count in most_common_pairs if count == max_freq]

                    # Choose the one with the highest numerical value if tied
                    fill_color = max(candidate_colors)

            # v. Fill the interior region in the output grid if fill_color determined
            if fill_color is not None:
                for r, c in interior_region_pixels:
                    output_grid[r, c] = fill_color
            # If no markers were found (fill_color is None), the interior
            # remains white (0) as initialized in the output grid. This is
            # different from the previous logic, but matches the refined rule
            # where only boundary + filled interior are preserved. Example 1's
            # top-right shape has no markers and its interior becomes white.

    # 4. Pixels of unclosed shapes are implicitly ignored as they are never copied.
    # 5. Pixels not part of a closed boundary or filled interior remain white.
    # 6. Return the completed output grid
    return output_grid