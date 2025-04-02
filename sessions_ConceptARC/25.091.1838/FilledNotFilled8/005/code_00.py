import numpy as np
from scipy.spatial import ConvexHull
from collections import deque

"""
Transforms the input grid based on the connectivity of its non-background pixels (assuming white '0' is background).

1.  Identify all non-background pixels and their unique color `C`.
2.  Determine the number of connected components formed by these pixels using 8-way adjacency (horizontal, vertical, diagonal).
3.  If there is exactly one connected component:
    - The output grid contains only the boundary pixels of that component, colored `C`.
    - A pixel is considered a boundary pixel if it's a non-background pixel adjacent (8-way) to at least one background pixel or the grid edge.
    - All other pixels in the output grid are background color.
4.  If there is more than one connected component (or isolated pixels):
    - Calculate the convex hull polygon enclosing all non-background pixel coordinates.
    - The output grid contains all pixels inside or on the boundary of this convex hull, colored `C`.
    - All other pixels are background color.
    - If there are fewer than 3 non-background pixels, or if the convex hull calculation fails (e.g., collinear points), only the original non-background pixels are colored `C` in the output.
5.  If there are no non-background pixels, the input grid is returned unchanged.
"""

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
        print(f"Warning: Multiple non-background colors {unique_colors}. Using {main_color}.")
        # Adjust coords if only main_color pixels should be considered (not needed based on examples)
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
                        # Boundary checks are implicit as coords not in set won't be processed
                        if neighbor_coord in non_bg_coords_set and neighbor_coord not in visited:
                            visited.add(neighbor_coord)
                            queue.append(neighbor_coord)
    return num_components

def find_outline(grid_np, non_bg_coords_list, color, background_color=0):
    """Keeps only boundary pixels of a single connected component."""
    output_grid = np.full(grid_np.shape, background_color, dtype=int)
    rows, cols = grid_np.shape

    for r, c in non_bg_coords_list:
        is_boundary = False
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = r + dr, c + dc

                # Check if neighbor is outside grid bounds
                if not (0 <= nr < rows and 0 <= nc < cols):
                    is_boundary = True
                    break
                # Check if neighbor is background color
                elif grid_np[nr, nc] == background_color:
                    is_boundary = True
                    break
            if is_boundary:
                break # Found a boundary condition

        if is_boundary:
            output_grid[r, c] = color

    return output_grid

def is_point_in_polygon(point, polygon_vertices):
    """
    Checks if a point is inside a polygon using the Ray Casting algorithm.
    Handles points on the boundary as inside.
    Args:
        point (tuple): (row, col) of the point to check.
        polygon_vertices (list): List of (row, col) tuples defining the polygon vertices in order.
    Returns:
        bool: True if the point is inside or on the boundary, False otherwise.
    """
    pr, pc = point
    num_vertices = len(polygon_vertices)
    intersections = 0

    for i in range(num_vertices):
        p1 = polygon_vertices[i]
        p2 = polygon_vertices[(i + 1) % num_vertices]
        r1, c1 = p1
        r2, c2 = p2

        # Check if point is a vertex
        if (pr, pc) == p1:
            return True
            
        # Check if point lies on a horizontal edge
        if r1 == r2 == pr and min(c1, c2) <= pc <= max(c1, c2):
            return True

        # Check if point lies on a vertical edge
        if c1 == c2 == pc and min(r1, r2) <= pr <= max(r1, r2):
             return True
             
        # Standard ray casting intersection check
        if min(r1, r2) <= pr < max(r1, r2): # Ray must cross edge vertically
            # Calculate intersection column (x-coordinate)
            # Avoid division by zero for vertical lines (handled by on-edge check above)
            if r1 != r2:
                 c_intersect = (pr - r1) * (c2 - c1) / (r2 - r1) + c1
                 # Count intersection if it's to the right of or at the point's column
                 if c_intersect >= pc:
                      intersections += 1

    return intersections % 2 == 1


def fill_convex_hull(grid_shape, non_bg_coords_list, color, background_color=0):
    """Fills the convex hull of the given coordinates."""
    output_grid = np.full(grid_shape, background_color, dtype=int)
    rows, cols = grid_shape

    if not non_bg_coords_list:
        return output_grid

    points = np.array(non_bg_coords_list)

    # Fallback: Color original points if < 3 points or hull fails
    def color_original_points():
        for r, c in non_bg_coords_list:
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = color
        return output_grid

    if len(points) < 3:
        return color_original_points()

    try:
        hull = ConvexHull(points)
        # Get vertices in order (ConvexHull provides this)
        hull_vertices_indices = hull.vertices
        hull_vertices = [tuple(map(int, points[i])) for i in hull_vertices_indices]

        # Find bounding box of the hull for efficiency
        min_r = int(np.min(points[hull_vertices_indices, 0]))
        max_r = int(np.max(points[hull_vertices_indices, 0]))
        min_c = int(np.min(points[hull_vertices_indices, 1]))
        max_c = int(np.max(points[hull_vertices_indices, 1]))

        # Iterate through pixels within the bounding box
        for r in range(max(0, min_r), min(rows, max_r + 1)):
            for c in range(max(0, min_c), min(cols, max_c + 1)):
                if is_point_in_polygon((r, c), hull_vertices):
                    output_grid[r, c] = color

    except Exception as e:
        # Catch scipy errors (e.g., QhullError for collinear points)
        print(f"Convex Hull calculation/filling failed: {e}. Coloring original points.")
        return color_original_points()

    return output_grid


def transform(input_grid):
    # Convert input to numpy array
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    background_color = 0

    # Find non-background pixels, their color, and a set of coordinates
    non_bg_coords_list, color, non_bg_coords_set = find_non_background_pixels(input_grid_np, background_color)

    # Handle empty case
    if not non_bg_coords_list:
        return input_grid # Return original grid

    # Check connectivity
    num_components = check_connectivity(input_grid_np.shape, non_bg_coords_list, non_bg_coords_set)

    # Apply transformation based on connectivity
    if num_components == 1:
        # Single component -> Find outline
        output_grid_np = find_outline(input_grid_np, non_bg_coords_list, color, background_color)
    else: # num_components > 1 or potentially 0 (handled by empty check)
        # Multiple components -> Fill convex hull
        output_grid_np = fill_convex_hull(input_grid_np.shape, non_bg_coords_list, color, background_color)

    # Convert result back to list of lists
    output_grid = output_grid_np.tolist()
    return output_grid