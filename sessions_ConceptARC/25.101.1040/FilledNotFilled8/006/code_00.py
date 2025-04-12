import numpy as np
from typing import List, Tuple, Set

# Assuming scipy/skimage are available for this verification
try:
    from scipy.spatial import ConvexHull
    from skimage.draw import polygon
    _SCIPY_AVAILABLE = True
except ImportError:
    _SCIPY_AVAILABLE = False
    print("Scipy/Skimage not available, cannot perform hull/vertex checks.")
    # Dummy classes if needed, though not strictly necessary for this check
    class ConvexHull:
         def __init__(self, points): self.vertices = []; self.simplices = np.array([]) # Add simplices
    def polygon(r, c, shape=None): return np.array([], dtype=int), np.array([], dtype=int)

# --- Helper Functions (abbreviated, assume they exist) ---
def _find_object_pixels(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]], np.ndarray]:
    object_color = -1
    object_pixels = set()
    points_list = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                if object_color == -1: object_color = grid[r, c]
                if grid[r, c] == object_color:
                     object_pixels.add((r, c))
                     points_list.append([c, r]) # Use (x,y) for geometric points
    if object_color == -1: object_color = 0
    # Convert points to numpy array for ConvexHull
    points_np = np.array(points_list)
    return object_color, object_pixels, points_np

def _fill_convex_hull(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int, points_np: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Fills hull and returns filled grid AND hull vertices coordinates."""
    hull_vertices_coords = np.array([]) # Store vertex coords (c, r)
    if not _SCIPY_AVAILABLE or len(object_pixels) < 3:
        return grid.copy(), hull_vertices_coords # Return copy and empty vertices

    output_grid = grid.copy()
    height, width = grid.shape

    try:
        hull = ConvexHull(points_np)
        # Get the coordinates of the hull vertices (use hull.vertices indices into points_np)
        hull_vertices_coords = points_np[hull.vertices] # These are (c, r)

        rr, cc = polygon(hull_vertices_coords[:, 1], hull_vertices_coords[:, 0], output_grid.shape)
        output_grid[rr, cc] = object_color
    except Exception as e:
        print(f"Hull calculation failed: {e}")
        return grid.copy(), hull_vertices_coords # Return copy and potentially empty/partial vertices

    return output_grid, hull_vertices_coords

# --- Inputs ---
train_1_input = np.array([
    [0,0,0,0,0,6,0,0,0,0,0,0,0],[0,0,0,0,0,0,6,0,0,0,0,0,0],[0,0,0,0,0,0,0,6,0,0,0,0,0],[0,0,6,0,0,0,0,0,6,0,0,0,0],[0,0,0,6,0,0,0,0,0,6,0,0,0],[0,0,0,0,6,0,0,0,0,0,6,0,0],[0,0,0,0,0,6,0,0,0,0,0,0,0],[0,0,0,0,0,0,6,0,0,0,0,0,0],[0,0,0,0,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0]
])
train_1_expected_output = np.array([
    [0,0,0,0,0,6,0,0,0,0,0,0,0],[0,0,0,0,6,6,6,0,0,0,0,0,0],[0,0,0,6,6,6,6,6,0,0,0,0,0],[0,0,6,6,6,6,6,6,6,0,0,0,0],[0,0,0,6,6,6,6,6,6,6,0,0,0],[0,0,0,0,6,6,6,6,6,6,6,0,0],[0,0,0,0,0,6,6,6,6,6,0,0,0],[0,0,0,0,0,0,6,6,6,0,0,0,0],[0,0,0,0,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0]
])

train_2_input = np.array([
    [0,0,0,0,0,3,0,0,0,0,0,0],[0,0,0,0,3,3,3,0,0,0,0,0],[0,0,0,3,3,3,3,3,0,0,0,0],[0,0,3,3,3,3,3,0,0,0,0,0],[0,3,3,3,3,3,0,0,0,0,0,0],[0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,3,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]
])
train_2_expected_output = np.array([
    [0,0,0,0,0,3,0,0,0,0,0,0],[0,0,0,0,3,0,0,0,0,0,0,0],[0,0,0,3,0,0,0,3,0,0,0,0],[0,0,3,0,0,0,3,0,0,0,0,0],[0,3,0,0,0,3,0,0,0,0,0,0],[0,0,0,0,3,0,0,0,0,0,0,0],[0,0,0,3,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]
])

print("--- Analysis ---")

if not _SCIPY_AVAILABLE:
    print("Cannot proceed with analysis due to missing libraries.")
else:
    # Example 1 Analysis
    print("\nExample 1:")
    obj_color_1, obj_pixels_1, points_1 = _find_object_pixels(train_1_input)
    hull_grid_1, vertices_1 = _fill_convex_hull(train_1_input, obj_pixels_1, obj_color_1, points_1)
    input_matches_hull_1 = np.array_equal(train_1_input, hull_grid_1)
    hull_matches_expected_1 = np.array_equal(hull_grid_1, train_1_expected_output)
    print(f"Input matches Hull Fill: {input_matches_hull_1}")
    print(f"Hull Fill matches Expected Output: {hull_matches_expected_1}")
    vertices_coords_1 = set((int(round(v[1])), int(round(v[0]))) for v in vertices_1) # Convert (c,r) back to (r,c)
    print(f"Hull Vertices (r, c): {sorted(list(vertices_coords_1))}")


    # Example 2 Analysis
    print("\nExample 2:")
    obj_color_2, obj_pixels_2, points_2 = _find_object_pixels(train_2_input)
    hull_grid_2, vertices_2 = _fill_convex_hull(train_2_input, obj_pixels_2, obj_color_2, points_2)
    input_matches_hull_2 = np.array_equal(train_2_input, hull_grid_2)
    print(f"Input matches Hull Fill: {input_matches_hull_2}")

    # Create grid from vertices
    vertices_grid_2 = np.zeros_like(train_2_input)
    vertices_coords_2 = set()
    if vertices_2.size > 0:
       # Convert vertices (c, r) float to (r, c) int for grid indexing
       # Rounding handles potential floating point inaccuracies near pixel centers
       vertices_coords_2 = set( (int(round(v[1])), int(round(v[0]))) for v in vertices_2 )
       for r, c in vertices_coords_2:
            if 0 <= r < vertices_grid_2.shape[0] and 0 <= c < vertices_grid_2.shape[1]:
                 vertices_grid_2[r, c] = obj_color_2
            else:
                 print(f"Warning: Vertex coord ({r},{c}) out of bounds.")


    vertices_match_expected_2 = np.array_equal(vertices_grid_2, train_2_expected_output)
    print(f"Grid from Hull Vertices matches Expected Output: {vertices_match_expected_2}")
    print(f"Hull Vertices (r, c): {sorted(list(vertices_coords_2))}")

    # Compare expected output pixels with vertices
    expected_pixels_2 = set(tuple(coord) for coord in np.argwhere(train_2_expected_output == obj_color_2))
    print(f"Expected Output Pixels (r, c): {sorted(list(expected_pixels_2))}")
    print(f"Vertices match Expected Pixels: {vertices_coords_2 == expected_pixels_2}")