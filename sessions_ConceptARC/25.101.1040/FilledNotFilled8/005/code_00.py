"""
Transformation rule:
1. Identify the primary non-background color (C) and the set of coordinates `P` for all pixels of this color within the input grid. Assume the rest of the grid is background (0).
2. Determine if the object is "solid" or "hollow": Check if any pixel in `P` has all 8 of its neighbours also having color C. If yes, the object is "solid"; otherwise, it is "hollow".
3. If the object is "solid":
    a. Create a new output grid initialized with the background color (0).
    b. For each pixel coordinate `(r, c)` in the input set `P`: If `(r, c)` has at least one neighbour (8 directions) in the input grid with the background color (0), set the pixel `(r, c)` in the output grid to color C.
    c. The resulting output grid is the outline.
4. If the object is "hollow":
    a. **(Requires `scipy` and `skimage` libraries)**
    b. Create a new output grid by copying the input grid.
    c. Treat the coordinates in `P` as points. Calculate the convex hull polygon enclosing these points.
    d. Identify all grid cells `(r', c')` that fall inside or on the boundary of this convex hull polygon.
    e. Set the color of each identified cell `(r', c')` in the output grid to C.
    f. The resulting output grid is the filled shape.
    g. **(Fallback if libraries unavailable):** Return the original input grid.
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
    class ConvexHull:
         def __init__(self, points):
             # Minimal implementation for structure, won't be used if _SCIPY_AVAILABLE is False
             self.vertices = [] # Provide vertices attribute
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
            # Skip the center pixel itself
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            # Check grid boundaries
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
            pixel_value = grid[r, c]
            if pixel_value != 0:
                # Assign the first non-zero color found as the object color
                if object_color == -1:
                    object_color = pixel_value
                
                # Add pixel coordinate if it matches the determined object color
                # (Assumes only one non-background color forms the main object)
                if pixel_value == object_color:
                     object_pixels.add((r, c))

    # Handle case where grid is all background (no object found)
    if object_color == -1:
        object_color = 0 # Default to background color

    return object_color, object_pixels

def _is_solid(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> bool:
    """Check if any object pixel has all 8 neighbors of the same object color."""
    height, width = grid.shape
    # An empty object cannot be solid
    if not object_pixels: 
        return False

    # Check each object pixel
    for r, c in object_pixels:
        neighbors = _get_neighbors(r, c, height, width)
        
        # An interior pixel must have exactly 8 neighbors within the grid boundaries
        if len(neighbors) == 8:
            all_neighbors_are_object_color = True
            # Check if all neighbors have the object color
            for nr, nc in neighbors:
                if grid[nr, nc] != object_color:
                    all_neighbors_are_object_color = False
                    break # No need to check further neighbors for this pixel
            
            # If all 8 neighbors matched, we found an interior pixel, the object is solid
            if all_neighbors_are_object_color:
                return True
                
    # If no interior pixel was found after checking all object pixels, it's hollow
    return False

def _create_outline(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> np.ndarray:
    """Keep only object pixels that are adjacent to a background pixel."""
    height, width = grid.shape
    # Start with a grid filled with the background color
    output_grid = np.zeros_like(grid) 

    # Iterate through the coordinates of the original object pixels
    for r, c in object_pixels:
        is_boundary = False
        neighbors = _get_neighbors(r, c, height, width)
        # Check if any neighbor in the *input* grid is background (color 0)
        for nr, nc in neighbors:
            if grid[nr, nc] == 0:
                is_boundary = True
                break # Found a background neighbor, no need to check others
        
        # If it's a boundary pixel, set its color in the output grid
        if is_boundary:
            output_grid[r, c] = object_color
            
    return output_grid

def _fill_convex_hull(grid: np.ndarray, object_pixels: Set[Tuple[int, int]], object_color: int) -> np.ndarray:
    """Fill the convex hull defined by the object pixels."""
    # Check if necessary libraries are available
    if not _SCIPY_AVAILABLE:
        print("Warning: Scipy/Scikit-image not available. Cannot compute convex hull. Returning original grid.")
        # Fallback behavior: return the input grid unchanged
        return grid

    height, width = grid.shape
    # Start with a copy of the input grid to preserve original points
    output_grid = grid.copy() 

    # Convex hull calculation requires at least 3 points to define a polygon
    if len(object_pixels) < 3:
        # If fewer than 3 points, filling is ill-defined or trivial.
        # Returning the input grid (which contains the 1 or 2 points) is reasonable.
        return output_grid

    # Convert pixel coordinates (row, col) to geometric points (x, y -> col, row)
    points = np.array([[c, r] for r, c in object_pixels])

    try:
        # Calculate the convex hull of the points
        hull = ConvexHull(points)
        # Get the coordinates of the vertices forming the hull boundary
        hull_vertices_coords = points[hull.vertices]

        # Get row and column indices of all pixels *inside* or *on the boundary* 
        # of the polygon defined by the hull vertices.
        # Note the order for skimage.draw.polygon: rows (y), then columns (x)
        rr, cc = polygon(hull_vertices_coords[:, 1], hull_vertices_coords[:, 0], output_grid.shape)

        # Fill the pixels within the calculated polygon area with the object color
        output_grid[rr, cc] = object_color
        
    except Exception as e:
        # Handle potential errors during hull calculation (e.g., QhullError for collinear points)
        print(f"Warning: Convex hull calculation failed ({e}). Returning original grid.")
        # Fallback: return the original grid if hull/fill fails
        return grid

    return output_grid

# === Main Transformation Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape

    # Step 1: Identify the object color and its pixel coordinates
    object_color, object_pixels = _find_object_pixels(grid_np)

    # Handle edge case: grid is empty or contains only background
    if object_color == 0 or not object_pixels:
        return input_grid # Return the original grid unchanged

    # Step 2: Determine if the object is "solid" (has interior pixels) or "hollow"
    is_input_solid = _is_solid(grid_np, object_pixels, object_color)

    # Step 3: Apply the transformation based on solidity
    if is_input_solid:
        # If the input object is solid, create its outline
        output_grid_np = _create_outline(grid_np, object_pixels, object_color)
    else:
        # If the input object is hollow, fill its convex hull
        # This step depends on scipy and skimage
        output_grid_np = _fill_convex_hull(grid_np, object_pixels, object_color)

    # Convert the resulting NumPy array back to a list of lists for the final output format
    output_grid = output_grid_np.tolist()
    
    return output_grid