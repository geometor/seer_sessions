import numpy as np
from scipy.spatial import ConvexHull
from collections import deque

"""
Transforms the input grid based on the connectivity of its non-background pixels (assuming white '0' is background).

1.  Identify all non-background pixels and their unique color `C`.
2.  Determine the number of connected components formed by these pixels using 8-way adjacency (horizontal, vertical, diagonal).
3.  If there is exactly one connected component:
    - The output grid contains the original non-background pixels minus the "interior" pixels.
    - An "interior" pixel is a non-background pixel where all 8 of its neighbors are within the grid boundaries and are also non-background pixels of color `C`.
    - All other pixels in the output grid are background color.
4.  If there is more than one connected component (or isolated pixels):
    - Calculate the convex hull polygon enclosing all non-background pixel coordinates.
    - The output grid contains all pixels whose centers fall inside or on the boundary of this convex hull, colored `C`.
    - All other pixels are background color.
    - If there are fewer than 3 non-background pixels, or if the convex hull calculation fails (e.g., collinear points), only the original non-background pixels are colored `C` in the output.
5.  If there are no non-background pixels, the input grid is returned unchanged.
"""

# === Helper Functions ===

def find_non_background_pixels(grid_np, background_color=0):
    """Finds coordinates and the unique color of non-background pixels."""
    coords = np.argwhere(grid_np != background_color)
    if coords.size == 0:
        return [], -1, set() # No non-background pixels

    colors = grid_np[coords[:, 0], coords[:, 1]]
    unique_colors = np.unique(colors)

    if len(unique_colors) == 1:
        main_color = int(unique_colors[0])
    elif len(unique_colors) > 1:
        # Task examples imply single color, take the first one if multiple exist
        main_color = int(unique_colors[0])
        # Keep all coords, but use main_color for output.
    else:
        return [], -1, set() # Should not happen

    # Return coordinates as list of tuples and set for quick lookup
    coord_list = [tuple(map(int, coord)) for coord in coords]
    coord_set = set(coord_list)
    return coord_list, main_color, coord_set

def check_connectivity(grid_shape, non_bg_coords_list, non_bg_coords_set):
    """Checks the connectivity of non-background pixels using BFS (8-way adjacency)."""
    if not non_bg_coords_list:
        return 0

    rows, cols = grid_shape
    visited = set()
    num_components = 0

    for start_coord in non_bg_coords_list:
        if start_coord not in visited:
            num_components += 1
            queue = deque([start_coord])
            visited.add(start_coord)

            while queue:
                r, c = queue.popleft()

                # Explore 8 neighbors
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue # Skip self

                        nr, nc = r + dr, c + dc
                        neighbor_coord = (nr, nc)

                        # Check if neighbor is a non-background pixel and not visited
                        if neighbor_coord in non_bg_coords_set and neighbor_coord not in visited:
                            visited.add(neighbor_coord)
                            queue.append(neighbor_coord)
    return num_components

def find_thin_outline(grid_np, non_bg_coords_list, color, background_color=0):
    """Removes interior pixels from a single connected component."""
    output_grid = grid_np.copy() # Start with a copy of the input
    rows, cols = grid_np.shape

    for r, c in non_bg_coords_list:
        is_interior = True
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc

                # Check if neighbor is outside grid bounds or is background
                if not (0 <= nr < rows and 0 <= nc < cols) or grid_np[nr, nc] == background_color:
                    is_interior = False # Found a neighbor that makes it non-interior
                    break
            if not is_interior:
                break # No need to check further neighbors for this pixel

        # If all neighbors were within bounds and non-background, it's interior
        if is_interior:
            output_grid[r, c] = background_color # Set interior pixel to background

    return output_grid

def is_point_in_polygon(point, polygon_vertices):
    """
    Checks if a point is inside a polygon using the Ray Casting algorithm.
    Handles points on the boundary as inside. Integer coordinates assumed.
    """
    pr, pc = point
    num_vertices = len(polygon_vertices)
    inside = False # Use standard ray casting state variable

    p1r, p1c = polygon_vertices[0]
    for i in range(num_vertices + 1):
        p2r, p2c = polygon_vertices[i % num_vertices]

        # Check if point is on a vertex
        if pr == p1r and pc == p1c:
            return True
            
        # Check if point is on a horizontal segment
        if pr == p1r == p2r and min(p1c, p2c) <= pc <= max(p1c, p2c):
             return True
             
        # Check if point is on a vertical segment
        if pc == p1c == p2c and min(p1r, p2r) <= pr <= max(p1r, p2r):
             return True

        # Ray casting logic: Check if the horizontal ray crosses the segment
        if min(p1r, p2r) <= pr < max(p1r, p2r): # Point's row is between segment's rows (exclusive upper bound)
             # Calculate the column intersection of the ray (at row pr) with the line segment
             # Avoid division by zero for vertical lines (handled by on-segment check)
            if p1r != p2r:
                c_intersect = (pr - p1r) * (p2c - p1c) / (p2r - p1r) + p1c
                # If intersection is at or to the right of the point's column, toggle inside state
                if c_intersect >= pc:
                    inside = not inside

        p1r, p1c = p2r, p2c # Move to next segment

    return inside


def fill_convex_hull(grid_shape, non_bg_coords_list, color, background_color=0):
    """Fills the convex hull of the given coordinates using ray casting."""
    output_grid = np.full(grid_shape, background_color, dtype=int)
    rows, cols = grid_shape

    if not non_bg_coords_list:
        return output_grid

    points = np.array(non_bg_coords_list)

    # --- Fallback function ---
    def color_original_points():
        out_fallback = np.full(grid_shape, background_color, dtype=int)
        for r, c in non_bg_coords_list:
            if 0 <= r < rows and 0 <= c < cols:
                out_fallback[r, c] = color
        return out_fallback

    # --- Handle few points case ---
    if len(points) < 3:
        return color_original_points()

    try:
        # --- Calculate Convex Hull ---
        hull = ConvexHull(points)
        # Get vertices in order
        hull_vertices_indices = hull.vertices
        # Use integer coordinates for polygon vertices
        hull_vertices = [tuple(map(int, points[i])) for i in hull_vertices_indices]

        # --- Find Bounding Box ---
        min_r = int(np.min(points[hull_vertices_indices, 0]))
        max_r = int(np.max(points[hull_vertices_indices, 0]))
        min_c = int(np.min(points[hull_vertices_indices, 1]))
        max_c = int(np.max(points[hull_vertices_indices, 1]))

        # --- Fill using Point-in-Polygon Test ---
        for r in range(max(0, min_r), min(rows, max_r + 1)):
            for c in range(max(0, min_c), min(cols, max_c + 1)):
                 # Check if the center of the pixel (r, c) is inside the polygon
                 # For grid coordinates, simply checking (r, c) is sufficient
                if is_point_in_polygon((r, c), hull_vertices):
                    output_grid[r, c] = color

    except Exception as e:
        # Catch scipy errors (e.g., QhullError for collinear points)
        # Use the fallback method if hull fails
        return color_original_points()

    return output_grid


# === Main Transform Function ===

def transform(input_grid):
    """
    Applies the transformation logic: thin outline for single component,
    convex hull fill for multiple components.
    """
    # Convert input list of lists to numpy array
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    background_color = 0 # Assuming background is always 0

    # --- Step 1: Find non-background pixels ---
    non_bg_coords_list, color, non_bg_coords_set = find_non_background_pixels(input_grid_np, background_color)

    # Handle empty case: return original grid if no non-bg pixels
    if not non_bg_coords_list:
        return input_grid

    # --- Step 2: Check connectivity ---
    num_components = check_connectivity(input_grid_np.shape, non_bg_coords_list, non_bg_coords_set)

    # --- Step 3 & 4: Apply transformation based on connectivity ---
    if num_components == 1:
        # Single component -> Find thin outline (remove interior pixels)
        output_grid_np = find_thin_outline(input_grid_np, non_bg_coords_list, color, background_color)
    else: # num_components > 1
        # Multiple components -> Fill convex hull
        output_grid_np = fill_convex_hull(input_grid_np.shape, non_bg_coords_list, color, background_color)

    # --- Step 5: Convert result back to list of lists ---
    output_grid = output_grid_np.tolist()
    return output_grid