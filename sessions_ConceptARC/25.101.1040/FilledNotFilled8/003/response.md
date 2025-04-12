```python
"""
Transformation rule:
1. Identify the primary non-white color (C) and the single contiguous object made of this color in the input grid.
2. Determine if the object is "solid" or "hollow".
    - An object is "solid" if at least one pixel of color C has all 8 of its neighbors also being color C.
    - Otherwise, the object is "hollow".
3. If the object is "solid", create an "outline" of the object.
    - The outline consists of only those pixels of color C from the input that were adjacent (8 directions) to at least one background pixel (0). All other pixels become background (0).
4. If the object is "hollow", create a "filled" version of the shape based on its convex hull.
    - Calculate the convex hull of the coordinates of the object pixels.
    - Fill the area within this convex hull with the object color C, preserving the original object pixels.
"""

import numpy as np
from typing import List, Tuple, Set

# Attempt to import optional libraries for convex hull calculation
try:
    from scipy.spatial import ConvexHull
    from skimage.draw import polygon
    _SCIPY_AVAILABLE = True
except ImportError:
    _SCIPY_AVAILABLE = False
    # Define dummy classes/functions if imports fail to avoid runtime errors later
    # This allows the code structure to remain, but hull calculation will fail gracefully.
    class ConvexHull:
         def __init__(self, points):
            pass
    def polygon(r, c, shape=None):
         # Return empty arrays if polygon can't be drawn
         return np.array([], dtype=int), np.array([], dtype=int)


# === Helper Functions ===

def _get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Get valid 8-directional neighbor coordinates."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def _find_object_pixels(grid: np.ndarray) -> Tuple[int, Set[Tuple[int, int]]]:
    """Find the non-background color and the set of coordinates for the object."""
    object_color = -1
    object_pixels = set()
    height, width = grid.shape

    # Iterate through the grid to find non-background pixels
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0:
                # Assign the first non-zero color found as the object color
                if object_color == -1:
                    object_color = grid[r, c]
                
                # Add pixel coordinate if it matches the object color
                # (Assumes only one non-background color forms the object)
                if grid[r, c] == object_color:
                     object_pixels.add((r, c))

    # Handle case where grid is all background
    if object_color == -1:
        object_color = 0 # Default to background color

    return object_color, object_pixels

def _is_solid(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> bool:
    """Check if any object pixel has all 8 neighbors of the same object color."""
    height, width = grid.shape
    if not object_pixels: return False # Empty object is not solid

    # Check each object pixel
    for r, c in object_pixels:
        neighbors = _get_neighbors(r, c, height, width)
        
        # An interior pixel must have exactly 8 neighbors within the grid
        if len(neighbors) == 8:
            all_neighbors_are_object_color = True
            # Check if all neighbors have the object color
            for nr, nc in neighbors:
                if grid[nr, nc] != object_color:
                    all_neighbors_are_object_color = False
                    break
            # If all neighbors match, we found an interior pixel, object is solid
            if all_neighbors_are_object_color:
                return True
                
    # If no interior pixel was found after checking all object pixels
    return False

def _create_outline(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> np.ndarray:
    """Keep only object pixels adjacent to background."""
    height, width = grid.shape
    output_grid = np.zeros_like(grid) # Start with all background

    # Iterate through the original object pixels
    for r, c in object_pixels:
        is_boundary = False
        neighbors = _get_neighbors(r, c, height, width)
        # Check if any neighbor is background (color 0)
        for nr, nc in neighbors:
            if grid[nr, nc] == 0:
                is_boundary = True
                break
        
        # If it's a boundary pixel, add it to the output
        if is_boundary:
            output_grid[r, c] = object_color
            
    return output_grid

def _fill_convex_hull(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> np.ndarray:
    """Fill the convex hull defined by the object pixels."""
    if not _SCIPY_AVAILABLE:
        print("Warning: Scipy/Scikit-image not available. Cannot compute convex hull. Returning original grid.")
        return grid # Or raise an error, or implement a fallback fill

    height, width = grid.shape
    output_grid = grid.copy() # Start with the input to preserve original points

    # Convex hull requires at least 3 points
    if len(object_pixels) < 3:
        # If fewer than 3 points, the concept of "filling" is ambiguous.
        # Based on the task (filling a hollow shape), returning the input
        # (which already contains the points) seems reasonable.
        return output_grid

    # Convert pixel coordinates (r, c) to points (x, y -> c, r) for geometric calculation
    points = np.array([[c, r] for r, c in object_pixels])

    try:
        # Calculate the convex hull
        hull = ConvexHull(points)
        # Get the coordinates of the hull vertices (use hull.vertices indices into points)
        hull_vertices_coords = points[hull.vertices]

        # Get row and column indices of pixels within the polygon defined by hull vertices
        # Note the order: polygon expects rows (y), then columns (x)
        rr, cc = polygon(hull_vertices_coords[:, 1], hull_vertices_coords[:, 0], output_grid.shape)

        # Fill the pixels inside the hull with the object color
        output_grid[rr, cc] = object_color
    except Exception as e:
        # Handle potential errors during hull calculation (e.g., collinear points)
        print(f"Warning: Convex hull calculation failed ({e}). Returning original grid.")
        # Fallback: return the original grid if hull/fill fails
        return grid

    return output_grid

# === Main Transformation Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by either filling a hollow shape (using convex hull) 
    or creating an outline of a solid shape.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Step 1: Identify the object color and its pixels
    object_color, object_pixels = _find_object_pixels(grid_np)

    # Handle edge case: no object found (grid is all background or empty)
    if object_color == 0 or not object_pixels:
        return input_grid # Return the original grid

    # Step 2: Determine if the object is solid or hollow
    solid = _is_solid(grid_np, object_pixels, object_color)

    # Step 3: Apply the appropriate transformation based on solidity
    if solid:
        # If solid, create the outline
        output_grid_np = _create_outline(grid_np, object_pixels, object_color)
    else:
        # If hollow, fill the convex hull
        output_grid_np = _fill_convex_hull(grid_np, object_pixels, object_color)

    # Convert the resulting NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid
```