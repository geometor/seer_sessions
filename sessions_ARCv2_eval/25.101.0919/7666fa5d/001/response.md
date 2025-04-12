```python
import numpy as np
from scipy.spatial import ConvexHull
from skimage.measure import label
from collections import Counter
from matplotlib.path import Path
import math

# Helper function to find the background color (most frequent color)
def find_background_color(grid: np.ndarray) -> int:
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    # Handle empty grid case if necessary, though ARC constraints likely prevent it
    if colors.size == 0:
        return 0 # Default assumption or raise error
    return colors[np.argmax(counts)]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies clusters of non-background 'marker' pixels using 8-connectivity. 
    For each cluster containing 3 or more marker points, it computes the 
    convex hull of the coordinates of these points. 
    It then iterates through all grid cells. If a cell's original color was the 
    background color and its center lies strictly inside the calculated convex 
    hull polygon for any cluster, its color is changed to red (2). 
    Otherwise, the cell's color remains unchanged.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # 1. Identify the background color
    background_color = find_background_color(input_array)
    fill_color = 2 # The color used for filling (red)

    # 2. Identify all unique marker colors
    marker_colors = np.unique(input_array[input_array != background_color])

    # If there are no marker colors, return the original grid
    if marker_colors.size == 0:
        return input_grid

    # 3. Process each marker color separately
    for marker_color in marker_colors:
        # 4a. Create a binary mask for the current marker color
        marker_mask = (input_array == marker_color)

        # 4b. Find connected components (clusters) using 8-connectivity
        # connectivity=2 corresponds to 8-connectivity in skimage.label
        labeled_mask, num_labels = label(marker_mask, connectivity=2, return_num=True)

        # 4c. Iterate through each identified cluster (labels 1 to num_labels)
        for i in range(1, num_labels + 1):
            # Get the (row, col) coordinates of pixels in the current cluster
            cluster_points_rc = np.argwhere(labeled_mask == i)

            # 4ci. Ensure cluster has enough points to form a polygon
            if len(cluster_points_rc) >= 3:
                # ConvexHull works with (x, y) coordinates, which correspond to (col, row)
                # Convert coordinates and use float type for geometric precision
                cluster_points_xy = cluster_points_rc[:, ::-1].astype(float) # Swap rc to xy (col, row)

                try:
                    # 4ci. Compute the convex hull of the cluster points
                    hull = ConvexHull(cluster_points_xy)
                    # Get the vertices defining the hull polygon
                    hull_vertices_xy = cluster_points_xy[hull.vertices]

                    # Create a matplotlib Path object for efficient point-in-polygon testing
                    hull_path = Path(hull_vertices_xy)

                    # 4cii. Find integer grid coordinates strictly inside the hull
                    # For efficiency, determine the bounding box of the hull
                    min_col, min_row = np.min(hull_vertices_xy, axis=0)
                    max_col, max_row = np.max(hull_vertices_xy, axis=0)
                    
                    # Define grid search bounds based on bounding box, clamped to grid dimensions
                    min_r_idx = max(0, math.floor(min_row))
                    max_r_idx = min(rows, math.ceil(max_row) + 1) # +1 because range is exclusive
                    min_c_idx = max(0, math.floor(min_col))
                    max_c_idx = min(cols, math.ceil(max_col) + 1) # +1 because range is exclusive

                    # Iterate through potentially relevant grid cells
                    for r in range(min_r_idx, max_r_idx):
                        for c in range(min_c_idx, max_c_idx):
                            # 4ciii. Check if the original pixel was background color
                            if input_array[r, c] == background_color:
                                # Test if the *center* of the pixel (col + 0.5, row + 0.5)
                                # lies strictly inside the hull polygon.
                                # Use a small negative radius for strict containment.
                                point_xy = (c + 0.5, r + 0.5)
                                if hull_path.contains_point(point_xy, radius=-1e-9):
                                    # 4ciii. (part 2) Change background pixel to fill color
                                    output_array[r, c] = fill_color

                except Exception:
                    # ConvexHull calculation can fail (e.g., all points collinear).
                    # In such cases, simply skip processing this cluster's fill.
                    # print(f"Warning: ConvexHull failed for cluster {i} of color {marker_color}. Skipping fill.")
                    pass # Continue to the next cluster or marker color

    # 5. Return the modified grid as a list of lists
    return output_array.tolist()
```