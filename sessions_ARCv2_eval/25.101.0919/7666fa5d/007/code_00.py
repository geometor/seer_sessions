"""
The transformation identifies clusters of non-background 'marker' pixels in the
input grid using 8-way connectivity. For each unique marker color, it finds
all connected groups (clusters) of pixels of that color. 

If a cluster contains 3 or more marker pixels, the transformation computes the
convex hull of the coordinates of these pixels. The coordinates are treated as
points (col + 0.5, row + 0.5) representing the center of each pixel cell.

Then, it identifies all grid cells (pixels) whose centers lie inside or exactly
on the boundary of this convex hull polygon. 

Finally, for each such identified grid cell, if its original color in the input
grid was the background color (the most frequent color in the input), its
color in the output grid is changed to red (color 2). All other pixels (original
marker pixels, background pixels outside any hull) retain their original color.
"""

import numpy as np
from scipy.spatial import ConvexHull
from matplotlib.path import Path 
import math
from collections import deque

def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid, assuming it's the background."""
    colors, counts = np.unique(grid, return_counts=True)
    if colors.size == 0:
        # Handle empty grid case if necessary, though ARC constraints likely prevent it
        return 0 # Default assumption or raise error
    # Ensure the returned color is a standard Python int
    return int(colors[np.argmax(counts)]) 

def find_connected_components(marker_mask: np.ndarray) -> list[list[tuple[int, int]]]:
    """
    Finds clusters of True values in a boolean mask using 8-way connectivity (BFS).

    Args:
        marker_mask: A 2D numpy array (boolean) where True indicates a marker pixel.

    Returns:
        A list of clusters, where each cluster is a list of (row, col) tuples.
    """
    rows, cols = marker_mask.shape
    visited = np.zeros_like(marker_mask, dtype=bool)
    clusters = []

    # Define 8 neighbors (horizontal, vertical, diagonal)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),
                 (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for r in range(rows):
        for c in range(cols):
            # If it's a marker pixel and not yet visited, start a new cluster search (BFS)
            if marker_mask[r, c] and not visited[r, c]:
                current_cluster = []
                q = deque([(r, c)])
                visited[r, c] = True
                current_cluster.append((r, c))

                while q:
                    curr_r, curr_c = q.popleft()

                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # If neighbor is a marker pixel and not visited
                            if marker_mask[nr, nc] and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                current_cluster.append((nr, nc))
                
                # Add the found cluster to the list if it's not empty
                if current_cluster:
                    clusters.append(current_cluster)
                    
    return clusters


def fill_convex_hull_path(output_array: np.ndarray, input_array: np.ndarray, 
                           hull_vertices_xy: np.ndarray, background_color: int, fill_color: int):
    """
    Fills the convex hull using matplotlib.path.Path.
    Checks pixel centers (c+0.5, r+0.5) for containment within the hull.

    Args:
        output_array: The grid to modify.
        input_array: The original input grid (for checking background color).
        hull_vertices_xy: Numpy array of hull vertices [(x, y), ...] i.e., [(col, row), ...].
        background_color: The color considered background.
        fill_color: The color to fill with.
    """
    rows, cols = output_array.shape
    hull_path = Path(hull_vertices_xy)

    # Determine bounding box of the hull for efficiency
    if hull_vertices_xy.shape[0] == 0: return # Skip if hull is empty
    min_col, min_row = np.min(hull_vertices_xy, axis=0)
    max_col, max_row = np.max(hull_vertices_xy, axis=0)
    
    # Define grid search bounds based on bounding box, clamped to grid dimensions
    # Use floor/ceil to ensure coverage, +1 for exclusive range end
    min_r_idx = max(0, math.floor(min_row))
    max_r_idx = min(rows, math.ceil(max_row) + 1) 
    min_c_idx = max(0, math.floor(min_col))
    max_c_idx = min(cols, math.ceil(max_col) + 1) 

    # Generate coordinates of pixel centers within the bounding box to check
    points_to_check_rc = []
    for r in range(min_r_idx, max_r_idx):
        for c in range(min_c_idx, max_c_idx):
             points_to_check_rc.append((r,c))
    
    if not points_to_check_rc:
        return # No points in bounding box to check

    points_to_check_rc_np = np.array(points_to_check_rc)
    # Convert grid center coords (r, c) to check points (x, y) = (c + 0.5, r + 0.5)
    points_to_check_xy = points_to_check_rc_np[:, ::-1] + 0.5 

    # Use contains_points for batch checking. 
    # Use a small positive radius to robustly include points on the boundary.
    containment_mask = hull_path.contains_points(points_to_check_xy, radius=1e-9) 

    # Get the (r, c) coordinates of pixel centers inside (or on boundary of) the hull
    points_inside_rc = points_to_check_rc_np[containment_mask]

    # Apply fill color only to background pixels within the identified points
    for r, c in points_inside_rc:
        # Ensure coordinates are valid indices (should be, due to bounding box logic)
        if 0 <= r < rows and 0 <= c < cols:
            # Check if the pixel in the *original* grid was background
            if input_array[r, c] == background_color:
                # Modify the *output* grid
                output_array[r, c] = fill_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_array = np.copy(input_array)
    rows, cols = input_array.shape
    
    # Define the color used for filling the hulls
    fill_color = 2 # Red

    # Step 1: Identify the background color (most frequent color)
    background_color = find_background_color(input_array)

    # Step 2: Identify all unique marker colors (non-background colors)
    unique_colors = np.unique(input_array)
    marker_colors = unique_colors[unique_colors != background_color]

    # If there are no marker colors, the grid remains unchanged
    if marker_colors.size == 0:
        return input_grid

    # Step 3: Process each marker color individually
    for marker_color in marker_colors:
        # 3a. Create a boolean mask highlighting pixels of the current marker color
        marker_mask = (input_array == marker_color)

        # 3b. Find connected components (clusters) of marker pixels using 8-way connectivity
        clusters = find_connected_components(marker_mask)

        # 3c. Process each cluster found for the current marker color
        for cluster_points_rc_list in clusters:
            # Clusters are lists of (row, col) tuples
            
            # 3ci. Hull requires at least 3 points to form a non-degenerate polygon
            if len(cluster_points_rc_list) >= 3:
                # Convert list of tuples to numpy array [(r1, c1), (r2, c2), ...]
                cluster_points_rc = np.array(cluster_points_rc_list)
                
                # ConvexHull and Path expect (x, y) coordinates, which correspond to (col, row)
                # Convert coordinates and use float type for geometric precision
                cluster_points_xy = cluster_points_rc[:, ::-1].astype(float) 
                
                try:
                    # 3ci.1. Compute the convex hull of the cluster points
                    # Input points are treated as vertices for the hull calculation
                    hull = ConvexHull(cluster_points_xy)
                    
                    # Get the vertices that define the hull polygon boundary, in (col, row) format
                    hull_vertices_xy = cluster_points_xy[hull.vertices]

                    # 3ci.2. Fill the computed convex hull
                    # This function modifies output_array in place
                    fill_convex_hull_path(output_array, input_array, hull_vertices_xy, background_color, fill_color)

                except Exception as e:
                    # ConvexHull calculation can fail if all points are collinear.
                    # In such cases, no filling occurs for this cluster, which is reasonable.
                    # print(f"Debug: ConvexHull failed for cluster (color {marker_color}): {e}")
                    pass # Continue to the next cluster

    # Step 4: Return the modified grid as a list of lists
    return output_array.tolist()