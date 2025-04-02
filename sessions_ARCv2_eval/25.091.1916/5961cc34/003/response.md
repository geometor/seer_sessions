```python
import numpy as np
from scipy.ndimage import label
from scipy.spatial import ConvexHull
from matplotlib.path import Path

"""
Transformation Rule:

1. Identify all distinct connected shapes composed of Blue (1) and Green (3) pixels. Treat these colors as equivalent for shape definition.
2. Count the total number of these distinct shapes.
3. Locate the single Yellow (4) pixel and identify its column index (the "Key Column").
4. Based on the shape count:
    a. If the count is exactly 1:
        - Create an output grid filled with the background color (Azure, 8).
        - Fill the entire Key Column with Red (2).
    b. If the count is greater than 1:
        - Create an output grid filled with the background color (Azure, 8).
        - Collect all coordinates (row, col) of the Blue (1) and Green (3) pixels.
        - If 3 or more such pixels exist:
            - Calculate the convex hull of these points.
            - Determine the bounding box (min/max row/col) enclosing the hull vertices.
            - Iterate through all integer grid coordinates (pixels) within this bounding box.
            - For each coordinate, check if it lies inside or on the boundary of the convex hull polygon.
            - If it does, set the corresponding pixel in the output grid to Red (2).
        - If fewer than 3 such pixels exist (cannot form a polygon):
            - Color only the original Blue/Green pixel locations Red (2) in the output grid.
"""

def find_objects(grid, colors):
    """
    Finds connected objects of specified colors in a grid using 8-way connectivity.

    Args:
        grid (np.ndarray): The input grid.
        colors (list or set): A list or set of color values to consider as part of the objects.

    Returns:
        tuple: A tuple containing:
            - labeled_array (np.ndarray): An array where each object is marked with a unique integer label.
            - num_objects (int): The total number of distinct objects found.
    """
    mask = np.isin(grid, list(colors))
    # Define connectivity structure (8-way including diagonals)
    structure = np.array([[1,1,1],
                          [1,1,1],
                          [1,1,1]], dtype=bool)
    labeled_array, num_objects = label(mask, structure=structure)
    return labeled_array, num_objects

def points_inside_hull(points, hull):
    """
    Generates grid points inside a convex hull.

    Args:
        points (np.ndarray): N x 2 array of points defining the hull vertices.
        hull (scipy.spatial.ConvexHull): The calculated convex hull object.

    Returns:
        list: A list of [row, col] coordinates inside or on the boundary of the hull.
    """
    path = Path(points[hull.vertices])
    
    # Determine bounding box
    min_r, min_c = np.min(points[hull.vertices], axis=0).astype(int)
    max_r, max_c = np.max(points[hull.vertices], axis=0).astype(int)

    inside_points = []
    # Iterate through grid points within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # Check if the center of the pixel (r, c) is inside the path
            # Use a small tolerance for points exactly on the boundary
            if path.contains_point([r, c], radius=1e-9): 
                inside_points.append([r, c])
                
    # Also explicitly add the original points that form the hull vertices
    # This ensures boundary points are definitely included, addressing potential floating point issues
    # Convert hull vertices back to original point coordinates if necessary
    for vertex_idx in hull.vertices:
        point = points[vertex_idx].astype(int) # Ensure integer coordinates
        if list(point) not in inside_points:
             inside_points.append(list(point))
             
    # Add the original shape points as well to ensure they are colored
    # This covers cases where points are inside the hull but not vertices
    # and helps with thin shapes or lines that might not be fully captured by contains_point test
    for r_orig, c_orig in zip(*np.where(np.isin(input_grid, list(shape_colors)))) :
        point = [r_orig, c_orig]
        if point not in inside_points:
            inside_points.append(point)

    return inside_points


def transform(input_grid):
    """
    Applies the transformation rule based on the count and configuration of Blue/Green shapes.

    Args:
        input_grid (np.ndarray): The input 2D grid.

    Returns:
        np.ndarray: The transformed 2D grid.
    """
    # Define colors
    global background_color, shape_colors, key_color, output_color # Make global for helper
    background_color = 8
    shape_colors = {1, 3}  # Blue and Green
    key_color = 4          # Yellow
    output_color = 2       # Red

    # Initialize output grid with the background color
    output_grid = np.full_like(input_grid, background_color)

    # Find and count the Blue/Green shapes
    labeled_shapes, num_shapes = find_objects(input_grid, shape_colors)

    # Find the location of the Yellow key pixel
    key_coords = np.where(input_grid == key_color)
    if len(key_coords[0]) == 0:
        # Should not happen based on examples, but handle defensively
        print("Warning: Key color (Yellow) not found.")
        return output_grid # Return background grid if key is missing

    key_col = key_coords[1][0] # Assume only one key pixel

    # --- Conditional Transformation ---
    if num_shapes == 1:
        # Case 1: Single shape -> Fill Key Column
        output_grid[:, key_col] = output_color
        
    elif num_shapes > 1:
        # Case 2: Multiple shapes -> Fill Convex Hull
        
        # Get coordinates of all blue/green pixels
        shape_pixel_coords_r, shape_pixel_coords_c = np.where(np.isin(input_grid, list(shape_colors)))
        
        # Check if we have enough points for a hull
        if len(shape_pixel_coords_r) >= 3:
            # Combine row and column coordinates into a list of [row, col] pairs
            points = np.vstack((shape_pixel_coords_r, shape_pixel_coords_c)).T
            
            try:
                # Calculate the convex hull
                hull = ConvexHull(points)
                
                # Find all integer grid points inside the hull
                fill_points = points_inside_hull(points, hull)
                
                # Color the identified points in the output grid
                for r, c in fill_points:
                    # Ensure coordinates are within grid bounds before coloring
                    if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
                        output_grid[r, c] = output_color
                        
            except Exception as e:
                 # This might happen if points are collinear, ConvexHull fails
                 print(f"ConvexHull calculation failed (possibly collinear points): {e}")
                 # Fallback: Just color the original shape pixels
                 output_grid[shape_pixel_coords_r, shape_pixel_coords_c] = output_color

        elif len(shape_pixel_coords_r) > 0: # Handle cases with 1 or 2 points (lines)
             # Fallback for too few points: Just color the original shape pixels
             output_grid[shape_pixel_coords_r, shape_pixel_coords_c] = output_color
             
    # If num_shapes == 0, the grid remains background color, which is correct.

    return output_grid
```