"""
Transformation Rule:

1. Identify the two distinct non-white colors (Color A, Color B) and their pixel locations (Coords A, Coords B) in the input grid.
2. Determine which object is 'interrupted' by the other by checking connectivity after temporarily removing the other object's pixels. The color of the object that becomes disconnected is the 'interrupted_color', and its coordinates are 'coords_interrupted'.
3. Calculate the bounding box (min/max row/col) of the 'interrupted' object (coords_interrupted).
4. Create the union of the pixel locations of both original non-white objects (Union Coords = Coords A U Coords B).
5. Filter the Union Coords, keeping only those coordinates that fall within the bounding box of the 'interrupted' object calculated in step 3. These are the 'output_coords'.
6. Create an output grid of the same dimensions as the input, filled with the background color (white, 0).
7. Fill the pixels corresponding to the 'output_coords' with the 'interrupted_color'.
"""

import numpy as np
from scipy.ndimage import label, generate_binary_structure
from typing import List, Tuple, Set, Optional

def find_colors(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """Finds the two distinct non-background (0) colors in the grid."""
    unique_colors = np.unique(grid)
    non_background_colors = unique_colors[unique_colors != 0]
    if len(non_background_colors) == 2:
        return tuple(int(c) for c in non_background_colors) # Cast to int
    else:
        return None

def get_pixel_coords(grid: np.ndarray, color: int) -> Set[Tuple[int, int]]:
    """Gets the coordinates of all pixels with the specified color."""
    rows, cols = np.where(grid == color)
    # Cast numpy int types to standard python int for consistency in sets
    return set(zip(map(int, rows), map(int, cols))) 

def is_connected(grid: np.ndarray, color: int) -> bool:
    """Checks if all pixels of a given color form a single connected component (4-connectivity)."""
    mask = (grid == color)
    if not np.any(mask):
        # Consistent with scipy.ndimage.label returning 0 features for empty input
        return True # Or arguably False if object must exist to be connected? Examples imply objects exist. Let's treat empty as 'not disconnected'.
        
    # von Neumann neighborhood (4-connectivity)
    connectivity_structure = generate_binary_structure(2, 1) 
    labeled_array, num_features = label(mask, structure=connectivity_structure)
    
    # Returns True if 0 or 1 component found
    return num_features <= 1

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """Calculates the min_row, min_col, max_row, max_col for a set of coordinates."""
    if not coords:
        return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def transform(input_grid: List[List[int]]) -> List[List[int]]:  
    """
    Transforms the input grid by identifying two overlapping objects, determining
    which one interrupts the other's connectivity, calculating the bounding box 
    of the interrupted object, and filling the union of both objects' pixels 
    within that bounding box with the interrupted object's color.
    """
    
    # Convert input to numpy array and get dimensions
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    background_color = 0

    # --- Step 1: Identify colors and coordinates ---
    colors = find_colors(grid_np)
    if colors is None:
        # Return background grid if not exactly two non-background colors
        return [[background_color for _ in range(width)] for _ in range(height)]
        
    color_a, color_b = colors
    coords_a = get_pixel_coords(grid_np, color_a)
    coords_b = get_pixel_coords(grid_np, color_b)
    
    if not coords_a or not coords_b:
        # Should not happen if find_colors found 2 colors, but check defensively
        return [[background_color for _ in range(width)] for _ in range(height)]

    # --- Step 2: Determine interrupted object ---
    # Check connectivity of A when B is removed
    temp_grid_a = grid_np.copy()
    for r, c in coords_b:
        temp_grid_a[r, c] = background_color
    a_remains_connected = is_connected(temp_grid_a, color_a)

    # Check connectivity of B when A is removed
    temp_grid_b = grid_np.copy()
    for r, c in coords_a:
        temp_grid_b[r, c] = background_color
    b_remains_connected = is_connected(temp_grid_b, color_b)

    interrupted_color: int = -1
    coords_interrupted: Set[Tuple[int, int]] = set()
    coords_interrupting: Set[Tuple[int, int]] = set()

    if not a_remains_connected and b_remains_connected:
        # B interrupted A. A is the 'interrupted' object.
        interrupted_color = color_a
        coords_interrupted = coords_a
        coords_interrupting = coords_b
    elif a_remains_connected and not b_remains_connected:
        # A interrupted B. B is the 'interrupted' object.
        interrupted_color = color_b
        coords_interrupted = coords_b
        coords_interrupting = coords_a
    else:
        # Ambiguous case (e.g., both connected, both disconnected) - return background
        return [[background_color for _ in range(width)] for _ in range(height)]
        
    # --- Step 3: Calculate bounding box of interrupted object ---
    bbox = get_bounding_box(coords_interrupted)
    if bbox is None: 
         # Should not happen if coords_interrupted is populated, but check defensively
        return [[background_color for _ in range(width)] for _ in range(height)]
    min_r, min_c, max_r, max_c = bbox

    # --- Step 4: Calculate union of all input object coordinates ---
    all_input_coords = coords_interrupted.union(coords_interrupting)

    # --- Step 5: Filter union coordinates by bounding box ---
    output_coords = set()
    for r, c in all_input_coords:
        if min_r <= r <= max_r and min_c <= c <= max_c:
            output_coords.add((r, c))

    # --- Step 6: Create output grid ---
    output_grid_np = np.full((height, width), background_color, dtype=int)

    # --- Step 7: Fill output coordinates with interrupted color ---
    for r, c in output_coords:
         # Check bounds just in case, though logic implies they should be valid
        if 0 <= r < height and 0 <= c < width:
            output_grid_np[r, c] = interrupted_color

    # Convert back to list of lists for the final output
    return output_grid_np.tolist()