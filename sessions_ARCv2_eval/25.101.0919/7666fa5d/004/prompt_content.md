
Previous Code:
```python
"""
Identifies clusters of non-background 'marker' pixels using 8-connectivity. 
For each cluster containing 3 or more marker points, it computes the 
convex hull of the coordinates of these points. 
It then iterates through all grid cells. If a cell's original color was the 
background color and its center lies strictly inside the calculated convex 
hull polygon for any cluster, its color is changed to red (2). 
Otherwise, the cell's color remains unchanged.
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
        return 0 # Default for empty grid
    return colors[np.argmax(counts)]

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
                
                # Add the found cluster to the list
                if current_cluster:
                    clusters.append(current_cluster)
                    
    return clusters


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the convex hull filling transformation based on marker pixel clusters.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_array = np.copy(input_array)
    rows, cols = input_array.shape
    
    # Define the color to use for filling
    fill_color = 2 # Red

    # Step 1: Identify the background color (most frequent)
    background_color = find_background_color(input_array)

    # Step 2: Identify all unique marker colors (non-background)
    unique_colors = np.unique(input_array)
    marker_colors = unique_colors[unique_colors != background_color]

    # If no marker colors, return the original grid
    if marker_colors.size == 0:
        return input_grid

    # Step 3: Process each marker color
    for marker_color in marker_colors:
        # 3a. Create a boolean mask for the current marker color
        marker_mask = (input_array == marker_color)

        # 3b. Find connected components (clusters) using 8-connectivity
        clusters = find_connected_components(marker_mask)

        # 3c. Process each cluster
        for cluster_points_rc in clusters:
            # 3ci. Ensure cluster has enough points to form a polygon
            if len(cluster_points_rc) >= 3:
                # Convert (row, col) tuples to a numpy array for ConvexHull
                cluster_points_np = np.array(cluster_points_rc)
                # ConvexHull expects (x, y) coordinates, which is (col, row)
                # Use float type for geometric precision
                cluster_points_xy = cluster_points_np[:, ::-1].astype(float) 
                
                try:
                    # 3ci.1. Compute the convex hull
                    hull = ConvexHull(cluster_points_xy)
                    # Get vertices defining the hull polygon
                    hull_vertices_xy = cluster_points_xy[hull.vertices]

                    # Create a matplotlib Path for efficient point-in-polygon testing
                    hull_path = Path(hull_vertices_xy)

                    # 3ci.2. Find integer grid coordinates strictly inside the hull
                    # Determine bounding box for efficiency
                    min_col, min_row = np.min(hull_vertices_xy, axis=0)
                    max_col, max_row = np.max(hull_vertices_xy, axis=0)
                    
                    # Define grid search bounds, clamped to grid dimensions
                    min_r_idx = max(0, math.floor(min_row))
                    max_r_idx = min(rows, math.ceil(max_row) + 1) # +1 for exclusive range
                    min_c_idx = max(0, math.floor(min_col))
                    max_c_idx = min(cols, math.ceil(max_col) + 1) # +1 for exclusive range

                    # Iterate through grid cells within the bounding box
                    for r in range(min_r_idx, max_r_idx):
                        for c in range(min_c_idx, max_c_idx):
                            # 3ci.4. Check if the original pixel was background
                            if input_array[r, c] == background_color:
                                # Test if the *center* of the pixel (col + 0.5, row + 0.5)
                                # lies strictly inside the hull polygon.
                                # Use a small negative radius for strict containment check.
                                point_xy = (c + 0.5, r + 0.5)
                                if hull_path.contains_point(point_xy, radius=-1e-9):
                                    # 3ci.4. Change background pixel to fill color in output
                                    output_array[r, c] = fill_color

                except Exception as e:
                    # ConvexHull can fail (e.g., collinear points). Ignore these cases.
                    # print(f"Debug: ConvexHull failed for cluster (color {marker_color}): {e}")
                    pass # Continue to the next cluster

    # Step 5: Return the modified grid as a list of lists
    return output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 4 8 8 8 4 8 8 8
8 8 8 8 8 8 8 4 8 8 8 4 8 8 8 4
8 8 8 8 8 8 8 8 8 8 4 8 8 8 4 8
8 8 8 8 8 8 8 8 8 4 8 8 8 4 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8
8 8 8 4 8 8 8 8 4 8 8 8 8 8 4 8
8 8 4 8 8 8 8 4 8 8 8 8 8 4 8 8
8 8 8 8 8 8 4 8 8 8 8 8 4 8 8 8
8 8 8 8 8 4 8 8 8 8 8 4 8 8 8 8
8 8 8 8 4 8 8 8 8 8 4 8 8 8 8 8
8 8 8 4 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 4 8 8 8 4 8 8 8
8 8 8 8 8 8 8 4 2 2 8 4 2 2 8 4
8 8 8 8 8 8 8 8 2 2 4 2 2 2 4 8
8 8 8 8 8 8 8 8 8 4 8 2 2 4 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8
8 8 8 4 2 2 8 8 4 8 8 8 8 8 4 8
8 8 4 2 2 2 2 4 2 2 8 8 8 4 8 8
8 8 8 2 2 2 4 2 2 2 2 8 4 8 8 8
8 8 8 8 2 4 2 2 2 2 2 4 8 8 8 8
8 8 8 8 4 8 2 2 2 2 4 8 8 8 8 8
8 8 8 4 8 8 8 2 2 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 4 8 8 8 4 8 8 8
8 8 8 8 8 8 8 4 8 8 8 4 8 8 8 4
8 8 8 8 8 8 8 8 8 8 4 8 8 8 4 8
8 8 8 8 8 8 8 8 8 4 8 8 8 4 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8
8 8 8 4 8 8 8 8 4 8 8 8 8 8 4 8
8 8 4 8 8 8 8 4 8 8 8 8 8 4 8 8
8 8 8 8 8 8 4 8 8 8 8 8 4 8 8 8
8 8 8 8 8 4 8 8 8 8 8 4 8 8 8 8
8 8 8 8 4 8 8 8 8 8 4 8 8 8 8 8
8 8 8 4 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 38
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 29.6875

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 3 8 8 8 8 8
8 8 8 8 3 8 8 8 8 3 8 8 8 8 8 8
8 8 8 3 8 8 8 8 3 8 8 8 8 8 8 8
8 8 3 8 8 8 8 3 8 8 8 8 8 8 8 8
8 3 8 8 8 8 3 8 8 8 8 8 8 8 8 8
3 8 8 8 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 3
8 8 8 8 8 8 3 8 8 8 8 8 8 8 3 8
8 8 8 8 8 3 8 8 8 8 8 8 8 3 8 8
8 8 8 8 3 8 8 8 8 8 8 8 3 8 8 8
8 8 8 3 8 8 8 8 8 8 8 3 8 8 8 8
8 8 3 8 8 8 8 8 8 8 3 8 8 8 8 8
8 3 8 8 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 3 8 8 8 8 8
8 8 8 8 3 8 8 8 8 3 8 8 8 8 8 8
8 8 8 3 2 2 8 8 3 2 2 8 8 8 8 8
8 8 3 2 2 2 2 3 2 2 2 2 8 8 8 8
8 3 2 2 2 2 3 2 2 2 2 2 2 8 8 8
3 2 2 2 2 2 2 2 2 3 2 2 2 2 8 8
8 2 2 2 2 2 2 2 3 2 2 2 2 2 2 8
8 8 2 2 2 2 2 3 2 2 2 2 2 2 2 3
8 8 8 2 2 2 3 2 2 2 2 2 2 2 3 8
8 8 8 8 2 3 2 2 2 2 2 2 2 3 8 8
8 8 8 8 3 2 2 2 2 2 2 2 3 8 8 8
8 8 8 3 8 2 2 2 2 2 2 3 8 8 8 8
8 8 3 8 8 8 2 2 2 2 3 8 8 8 8 8
8 3 8 8 8 8 8 2 2 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 3 8 8 8 8
8 8 8 8 8 8 8 8 8 8 3 8 8 8 8 8
8 8 8 8 3 8 8 8 8 3 8 8 8 8 8 8
8 8 8 3 8 8 8 8 3 8 8 8 8 8 8 8
8 8 3 8 8 8 8 3 8 8 8 8 8 8 8 8
8 3 8 8 8 8 3 8 8 8 8 8 8 8 8 8
3 8 8 8 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 8 8 8 8 8 8 8 3
8 8 8 8 8 8 3 8 8 8 8 8 8 8 3 8
8 8 8 8 8 3 8 8 8 8 8 8 8 3 8 8
8 8 8 8 3 8 8 8 8 8 8 8 3 8 8 8
8 8 8 3 8 8 8 8 8 8 8 3 8 8 8 8
8 8 3 8 8 8 8 8 8 8 3 8 8 8 8 8
8 3 8 8 8 8 8 8 8 3 8 8 8 8 8 8
8 8 8 8 8 8 8 8 3 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 96
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 75.0
