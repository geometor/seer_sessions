```python
"""
Identifies the non-background object in the input grid. Calculates the convex hull of the object's pixels.
If the input object perfectly matches its filled convex hull, the output is a grid containing only the pixels corresponding to the convex hull's vertices.
If the input object differs from its filled convex hull (i.e., it's "hollow" or sparse relative to its hull), the output is the grid representing the filled convex hull.
This process requires the numpy, scipy, and scikit-image libraries.
"""

import numpy as np
from typing import List, Tuple, Set, Optional

# Attempt to import optional libraries for convex hull calculation
try:
    from scipy.spatial import ConvexHull, QhullError
    from skimage.draw import polygon
    _LIBRARIES_AVAILABLE = True
except ImportError:
    _LIBRARIES_AVAILABLE = False
    # Define dummy classes/functions if imports fail to avoid runtime errors later
    class ConvexHull:
         def __init__(self, points): self.vertices = np.array([], dtype=int) # Provide vertices attribute
    class QhullError(Exception): pass
    def polygon(r, c, shape=None): return np.array([], dtype=int), np.array([], dtype=int)


def _find_object_pixels_and_points(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]], np.ndarray]:
    """
    Finds the non-background color, its pixel coordinates (r, c), and geometric points (c, r).

    Args:
        grid: The input NumPy array grid.

    Returns:
        A tuple containing:
        - object_color: The integer color value of the object (or 0 if none found).
        - object_pixels: A set of (row, col) tuples for the object pixels.
        - object_points: A NumPy array of [col, row] coordinates for geometric calculations.
                         Returns an empty array if no object pixels are found.
    """
    object_color = 0
    object_pixels = set()
    points_list = []
    height, width = grid.shape

    # Find the first non-background color
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                object_color = grid[r, c]
                break
        if object_color != 0:
            break

    # If no object color found, return early
    if object_color == 0:
        return 0, set(), np.array([])

    # Collect all pixels of the object color and their corresponding points
    for r in range(height):
        for c in range(width):
            if grid[r, c] == object_color:
                object_pixels.add((r, c))
                points_list.append([c, r]) # Use (x,y) -> (c,r) for geometry

    object_points = np.array(points_list)
    return object_color, object_pixels, object_points


def _calculate_and_fill_hull(
    points: np.ndarray, object_color: int, grid_shape: Tuple[int, int]
) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], Optional[np.ndarray]]:
    """
    Calculates the convex hull, returns the vertices, and a grid filled based on the hull.

    Args:
        points: NumPy array of [col, row] coordinates of the object.
        object_color: The color to fill the hull with.
        grid_shape: The (height, width) of the target grid.

    Returns:
        A tuple containing:
        - filled_hull_grid: NumPy array representing the filled convex hull, or None if calculation fails.
        - hull_vertex_points: NumPy array of [col, row] coordinates of hull vertices, or None.
        - hull: The ConvexHull object itself, or None.
    """
    if not _LIBRARIES_AVAILABLE:
        print("Warning: Required libraries (scipy, skimage) not available.")
        return None, None, None

    # Need at least 3 points for a non-degenerate hull
    if points.shape[0] < 3:
        # Handle cases with 0, 1, or 2 points - cannot form a hull polygon
        # We can return a grid with just those points marked
        filled_grid = np.zeros(grid_shape, dtype=int)
        vertex_points = points.copy() # Vertices are just the points themselves
        for c, r in points:
            if 0 <= int(r) < grid_shape[0] and 0 <= int(c) < grid_shape[1]:
                 filled_grid[int(r), int(c)] = object_color
        # Return the grid with points, the points as vertices, and None for hull object
        return filled_grid, vertex_points, None 

    try:
        # Calculate the convex hull
        hull = ConvexHull(points)
        # Get the coordinates [c, r] of the hull vertices
        hull_vertex_points = points[hull.vertices]

        # Create the filled hull grid
        filled_hull_grid = np.zeros(grid_shape, dtype=int)
        # Get row and column indices of pixels within the polygon defined by hull vertices
        # Note the order: polygon expects rows (y), then columns (x)
        rr, cc = polygon(hull_vertex_points[:, 1], hull_vertex_points[:, 0], grid_shape)
        # Fill the pixels inside the hull with the object color
        filled_hull_grid[rr, cc] = object_color
        
        return filled_hull_grid, hull_vertex_points, hull

    except QhullError as e:
        # Handle cases like collinear points where hull might be degenerate but calculable
        print(f"QhullError during convex hull calculation: {e}. Handling potential degenerate case.")
        # If it's collinear, hull might just be the line segment endpoints
        # Let's try to return a grid with just the input points marked.
        filled_grid = np.zeros(grid_shape, dtype=int)
        vertex_points = points.copy() # Treat all points as 'vertices' in this degenerate case
        for c, r in points:
             if 0 <= int(r) < grid_shape[0] and 0 <= int(c) < grid_shape[1]:
                 filled_grid[int(r), int(c)] = object_color
        return filled_grid, vertex_points, None # Indicate hull object wasn't standard

    except Exception as e:
        # Catch other potential errors during hull calculation
        print(f"Error during convex hull calculation: {e}")
        return None, None, None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on its relationship to its convex hull.
    If input matches filled hull -> output hull vertices.
    If input differs from filled hull -> output filled hull.
    Requires scipy and scikit-image.
    """
    # Convert input to NumPy array
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Step 1: Find object pixels and geometric points
    object_color, object_pixels, object_points = _find_object_pixels(grid_np)

    # Handle edge case: no object found
    if object_color == 0 or object_points.size == 0:
        return input_grid # Return original grid

    # Step 2: Calculate convex hull, get filled grid and vertices
    # This step requires scipy/skimage and handles cases < 3 points internally
    filled_hull_grid, hull_vertex_points, _ = _calculate_and_fill_hull(
        object_points, object_color, (height, width)
    )

    # Handle failure in hull calculation (e.g., libraries missing or unexpected error)
    if filled_hull_grid is None or hull_vertex_points is None:
         print("Fallback: Returning original grid due to hull calculation issues.")
         return input_grid # Fallback if hull calculation failed

    # Step 3: Compare input grid object pixels to the filled hull grid
    # Create a grid representing only the input object for accurate comparison
    input_object_only_grid = np.zeros_like(grid_np)
    for r, c in object_pixels:
        input_object_only_grid[r, c] = object_color

    # Check if the input object representation is identical to the filled hull
    is_solid_hull = np.array_equal(input_object_only_grid, filled_hull_grid)

    # Step 4: Determine output based on comparison
    if is_solid_hull:
        # Output: Grid containing only the hull vertices
        output_grid_np = np.zeros_like(grid_np)
        if hull_vertex_points.size > 0:
            for c, r in hull_vertex_points:
                 # Convert vertex coordinates (float) back to integer pixel indices
                 pr, pc = int(round(r)), int(round(c))
                 # Check bounds before assigning color
                 if 0 <= pr < height and 0 <= pc < width:
                      output_grid_np[pr, pc] = object_color
    else:
        # Output: The filled convex hull grid
        output_grid_np = filled_hull_grid

    # Convert final NumPy array back to list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
```