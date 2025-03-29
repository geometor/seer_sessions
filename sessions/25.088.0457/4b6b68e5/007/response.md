```python
import numpy as np
from collections import deque, Counter

"""
Identifies contiguous shapes of a single non-white color (boundaries) in the input grid.
Copies all found boundaries to the output grid.
Then, for each shape, determines if it encloses an interior region relative to the grid edges.
An interior region is defined as the set of pixels not belonging to the boundary itself and not reachable from the grid edges without crossing the boundary.

If a shape encloses an interior region:
1. Collect "marker" pixels from the *input* grid within this interior region. A marker pixel is any pixel whose color is not white (0) and not the same as the boundary's color.
2. Count the number of *distinct* marker colors found.
3. If there are two or more distinct marker colors:
   a. Count the frequency of each marker color.
   b. Determine the most frequent marker color.
   c. If there's a tie for the most frequent color, choose the color with the lowest numerical value among the tied colors. This is the "fill color".
   d. Fill the *entire* identified interior region in the *output* grid with this fill color.
4. If there are fewer than two distinct marker colors within the enclosed interior region (0 or 1):
   a. Fill the *entire* identified interior region in the *output* grid with white (0).

Pixels not part of any boundary and not part of any filled interior remain white (0).
Shapes that do not enclose an interior region simply have their boundaries drawn; their potential 'inside' areas (reachable from the grid edge) are not explicitly filled or cleared.
"""

def find_shapes_and_boundaries(grid):
    """
    Finds all distinct contiguous shapes of non-white colors using BFS.
    Returns a list of tuples, where each tuple contains:
    (set of boundary pixel coordinates, boundary_color)
    """
    H, W = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []

    for r in range(H):
        for c in range(W):
            # Start BFS from a non-white, unvisited pixel
            if grid[r, c] != 0 and not visited[r, c]:
                boundary_color = grid[r, c]
                current_shape_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_shape_pixels.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visited status, and if neighbor has the same color
                        if 0 <= nr < H and 0 <= nc < W and \
                           not visited[nr, nc] and \
                           grid[nr, nc] == boundary_color:
                            visited[nr, nc] = True
                            current_shape_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                # Add the found shape to the list
                if current_shape_pixels: 
                     shapes.append((current_shape_pixels, boundary_color))
    return shapes

def find_reachable(grid_shape, starts, impassable_pixels):
    """
    Finds all pixels reachable from start points without crossing impassable pixels using BFS.
    grid_shape is a tuple (H, W).
    starts is a list or set of (r, c) tuples (potential starting points).
    impassable_pixels is a set of (r, c) tuples (pixels that block movement).
    Returns a set of reachable (r, c) tuples.
    """
    H, W = grid_shape
    # Filter starts: must be within bounds and not impassable
    q = deque(p for p in starts if 0 <= p[0] < H and 0 <= p[1] < W and p not in impassable_pixels)
    reachable = set(q) # Initialize reachable with valid starting points
    
    # Use a visited array for efficiency
    visited = np.zeros(grid_shape, dtype=bool)
    for r_init, c_init in reachable:
        visited[r_init, c_init] = True

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
    An interior region is pixels not on the boundary and not reachable from the grid edges.
    Returns the set of interior pixels if the boundary encloses a region,
    otherwise returns an empty set.
    """
    H, W = grid_shape
    all_pixels = set((r, c) for r in range(H) for c in range(W))
    # Potential interior/exterior are all pixels EXCEPT the boundary itself
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

    # Find all pixels reachable from the edges without crossing the boundary
    # These are the exterior pixels (relative to this boundary)
    exterior_pixels = find_reachable(grid_shape, edge_starts, boundary_pixels)

    # The interior is whatever potential pixels are left after removing the exterior
    interior_pixels = potential_interior_exterior - exterior_pixels

    # If interior_pixels is not empty, the shape encloses a region w.r.t the grid boundary
    return interior_pixels


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    H, W = input_grid.shape
    # Initialize output grid with background color (white/0)
    output_grid = np.zeros_like(input_grid)

    # 1. Find all distinct shapes (boundaries) and their colors
    shapes = find_shapes_and_boundaries(input_grid)

    # 2. Draw all boundaries onto the output grid first
    for boundary_pixels, boundary_color in shapes:
        for r, c in boundary_pixels:
            # Basic bounds check for safety, though coordinates should be valid
            if 0 <= r < H and 0 <= c < W: 
                 output_grid[r, c] = boundary_color

    # 3. Process each shape again to handle interior filling
    for boundary_pixels, boundary_color in shapes:
        
        # 4. Determine if the shape encloses an interior region
        interior_region_pixels = get_interior_region((H, W), boundary_pixels)

        # 5. If an interior region exists:
        if interior_region_pixels:
            # a. Collect marker colors from the *input* grid within the interior region
            marker_colors = []
            for r, c in interior_region_pixels:
                # Bounds check just in case interior calculation yielded something odd
                if 0 <= r < H and 0 <= c < W: 
                    pixel_color = input_grid[r, c]
                    # A marker is non-white and not the boundary color
                    if pixel_color != 0 and pixel_color != boundary_color:
                        marker_colors.append(pixel_color)

            # b. Check the fill condition: at least two *distinct* marker colors
            distinct_marker_colors = set(marker_colors)
            
            fill_color = 0 # Default fill is white (0) if condition not met
            
            if len(distinct_marker_colors) >= 2:
                # c. Condition met: Determine the actual fill color
                if marker_colors: # Should be true if distinct_marker_colors >= 2
                    color_counts = Counter(marker_colors)
                    # Find the maximum frequency
                    max_freq = 0
                    # Find max frequency directly using Counter's values
                    if color_counts: # Check if counter is not empty
                         max_freq = max(color_counts.values())

                    # Find all colors with max frequency
                    candidate_colors = [color for color, count in color_counts.items() if count == max_freq]

                    # Tie-breaking: Choose the color with the *lowest* numerical value
                    if candidate_colors: # Ensure candidates exist
                         actual_fill_color = min(candidate_colors)
                         fill_color = actual_fill_color # Set fill color for the interior
            
            # d. Fill the interior region in the output grid with the determined color (either calculated or default white)
            for r, c in interior_region_pixels:
                 if 0 <= r < H and 0 <= c < W: # Bounds check for safety
                    output_grid[r, c] = fill_color

    # 6. Return the completed output grid
    return output_grid
```