
Previous Code:
```python
import numpy as np
from scipy.ndimage import label
from scipy.spatial import ConvexHull
from matplotlib.path import Path

"""
Transformation Rule:

1. Identify all distinct connected shapes composed of Blue (1) and Green (3) pixels using 8-way connectivity. Treat these colors as equivalent for shape definition.
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
            - For each coordinate, check if it lies inside or on the boundary of the convex hull polygon using matplotlib.path.
            - If it does, set the corresponding pixel in the output grid to Red (2).
            - Ensure original shape pixels are also colored Red (2) in the output.
        - If fewer than 3 such pixels exist (cannot form a polygon):
            - Color only the original Blue/Green pixel locations Red (2) in the output grid.
    c. If the count is 0:
        - Return the background grid.
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

def get_pixels_inside_hull(grid_shape, points, hull):
    """
    Generates integer grid coordinates inside or on the boundary of a convex hull polygon.

    Args:
        grid_shape (tuple): The (rows, cols) dimensions of the grid.
        points (np.ndarray): N x 2 array of points ([row, col]) that formed the hull.
        hull (scipy.spatial.ConvexHull): The calculated convex hull object.

    Returns:
        tuple: A tuple of (rows, cols) numpy arrays representing the coordinates inside the hull.
    """
    # Create a Path object from the hull vertices
    # Ensure the path is closed by repeating the first vertex at the end for contains_points
    hull_path = Path(np.vstack((points[hull.vertices], points[hull.vertices[0]])))

    # Determine bounding box based on the hull vertices for efficient checking
    min_coords = np.floor(np.min(points[hull.vertices], axis=0)).astype(int)
    max_coords = np.ceil(np.max(points[hull.vertices], axis=0)).astype(int)

    # Clamp bounding box coordinates to be within the grid dimensions
    min_r, min_c = np.maximum(0, min_coords)
    max_r, max_c = np.minimum(np.array(grid_shape) - 1, max_coords)

    # Generate a grid of points within the bounding box to test for inclusion
    rr, cc = np.meshgrid(np.arange(min_r, max_r + 1),
                         np.arange(min_c, max_c + 1),
                         indexing='ij') # 'ij' indexing aligns with numpy array (row, col)

    # Stack coordinates into a format suitable for contains_points
    test_points = np.vstack((rr.ravel(), cc.ravel())).T

    # Check which points fall inside or on the boundary of the hull path
    # A small radius helps include points exactly on the boundary
    inside_mask = hull_path.contains_points(test_points, radius=1e-9)

    # Get the coordinates of the points that tested positive
    inside_points_coords = test_points[inside_mask]

    # Combine the points found inside with the original points that define the shapes
    # This ensures all original shape pixels are included, especially for thin shapes or lines
    # not fully captured by the contains_points test on grid centers.
    all_fill_points = np.vstack((inside_points_coords, points))

    # Remove duplicates and convert to integer coordinates using rounding
    # Use a set of tuples for efficient duplicate removal
    unique_coords_set = set()
    for r, c in all_fill_points:
       rint, cint = int(round(r)), int(round(c)) # Round to nearest integer coordinates
       # Final check to ensure coordinates are within grid bounds after rounding
       if 0 <= rint < grid_shape[0] and 0 <= cint < grid_shape[1]:
           unique_coords_set.add((rint, cint))

    # If no points were identified, return empty arrays
    if not unique_coords_set:
        return (np.array([], dtype=int), np.array([], dtype=int))

    # Convert the set of unique coordinates back into separate row and column arrays
    final_rows, final_cols = zip(*unique_coords_set)
    return (np.array(final_rows), np.array(final_cols))


def transform(input_grid):
    """
    Applies the transformation rule based on the count and configuration of Blue/Green shapes.

    Args:
        input_grid (np.ndarray): The input 2D grid.

    Returns:
        np.ndarray: The transformed 2D grid.
    """
    # Define colors used in the task
    background_color = 8
    shape_colors = {1, 3}  # Blue and Green pixels define shapes
    key_color = 4          # Yellow pixel defines the key column
    output_color = 2       # Red is the output color for filled areas

    # Initialize the output grid with the same dimensions as the input, filled with background color
    output_grid = np.full_like(input_grid, background_color)

    # Identify and count distinct connected shapes made of Blue or Green pixels
    labeled_shapes, num_shapes = find_objects(input_grid, shape_colors)

    # Find the coordinates of the Yellow key pixel
    key_coords_r, key_coords_c = np.where(input_grid == key_color)

    # Check if the key pixel exists (should always be true based on examples)
    if len(key_coords_r) == 0:
        print("Warning: Key color (Yellow) not found.")
        # If key is missing, return the background grid as a safe default
        return output_grid

    # Extract the column index of the key pixel (assuming only one exists)
    key_col = key_coords_c[0]

    # --- Apply Transformation Based on Shape Count ---

    if num_shapes == 1:
        # Case 1: Exactly one shape found.
        # Fill the entire column identified by the key pixel with the output color.
        output_grid[:, key_col] = output_color

    elif num_shapes > 1:
        # Case 2: More than one shape found.
        # Fill the convex hull encompassing all shape pixels.

        # Get the coordinates of all pixels belonging to any Blue or Green shape
        shape_pixel_coords_r, shape_pixel_coords_c = np.where(np.isin(input_grid, list(shape_colors)))

        # Proceed only if there are actually shape pixels
        if len(shape_pixel_coords_r) > 0:
            # Check if there are enough points to form a convex hull polygon (at least 3)
            if len(shape_pixel_coords_r) >= 3:
                # Combine row and column coordinates into an N x 2 array of points
                points = np.vstack((shape_pixel_coords_r, shape_pixel_coords_c)).T

                try:
                    # Calculate the convex hull of the points.
                    # 'QJ' option asks Qhull to jitter points if it encounters precision issues (e.g., collinear points)
                    hull = ConvexHull(points, qhull_options='QJ')

                    # Determine all integer grid coordinates falling inside or on the boundary of this hull
                    fill_rows, fill_cols = get_pixels_inside_hull(input_grid.shape, points, hull)

                    # Color these identified pixels in the output grid with the output color
                    if len(fill_rows) > 0:
                        output_grid[fill_rows, fill_cols] = output_color

                except Exception as e:
                     # Handle cases where ConvexHull fails even with jittering (e.g., all points perfectly collinear)
                     print(f"ConvexHull calculation failed: {e}. Falling back to coloring original pixels.")
                     # As a fallback, just color the original shape pixels
                     output_grid[shape_pixel_coords_r, shape_pixel_coords_c] = output_color

            else: # Case 2b: Fewer than 3 shape pixels (1 or 2 points)
                 # Cannot form a hull polygon. Just color the original shape pixels.
                 output_grid[shape_pixel_coords_r, shape_pixel_coords_c] = output_color

    # Case 3: num_shapes == 0. No shapes found.
    # The output grid remains the initialized background color, which is correct.

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 4 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 3 3 8 8 8 8
8 1 1 1 1 8 8 8 1 1 1 3 8 8 8 8 8 8 1 1 1 1 8 8 8
8 1 1 1 1 8 8 8 1 1 1 3 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 1 1 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8
8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8
8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8
8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 126
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 43.82608695652175

## Example 3:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 1 1 1 1 1 1 8 8 8 8 8 8 3 1 1 1 1 1 8 8
8 8 1 1 1 1 1 1 8 8 8 8 8 8 3 1 1 1 1 1 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8
8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 113
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 44.664031620553374

## Example 4:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 1 1 1 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 3 1 1 1 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 76
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.039525691699623
