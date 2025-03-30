import numpy as np
from collections import defaultdict
import copy
import math

"""
Transformation Rule:

1.  Initialize the output grid as a copy of the input grid.
2.  Set all original blue (1) pixels in the output grid to white (0).
3.  Find all connected components (objects) in the input grid that are neither white (0) nor blue (1).
4.  For each object, calculate its canonical shape signature based on the relative coordinates of its pixels from its top-leftmost point.
5.  Group the identified objects based on having the exact same color and shape signature.
6.  Identify groups that contain exactly two objects (these are the pairs).
7.  For each identified pair of objects (Object A and Object B):
    a.  Determine the fixed translation (row offset `dr_obj`, column offset `dc_obj`) that maps the position of Object A's top-left corner to Object B's top-left corner.
    b.  Iterate through each pixel `(r_A, c_A)` belonging to Object A.
    c.  Find the corresponding pixel `(r_B, c_B)` in Object B using the translation: `r_B = r_A + dr_obj`, `c_B = c_A + dc_obj`.
    d.  Draw a line segment between the corresponding pixel pair `(r_A, c_A)` and `(r_B, c_B)` using a line drawing algorithm (Bresenham's).
    e.  The line drawing process involves:
        i. Calculating all integer pixel coordinates on the line segment using Bresenham's algorithm.
        ii. Iterating through the calculated points, *excluding* the start point `(r_A, c_A)` and the end point `(r_B, c_B)`.
        iii. For each intermediate point `(r_pixel, c_pixel)`:
            - Checking if the point is within the grid boundaries.
            - If the pixel `(r_pixel, c_pixel)` in the *output grid* is currently white (0), set its color to blue (1).
8.  Return the modified output grid.
"""

def find_objects(grid, ignore_colors={0}):
    """
    Finds connected objects of the same color in the grid, ignoring specified colors.

    Args:
        grid (np.ndarray): The input grid.
        ignore_colors (set): Set of color values to ignore.

    Returns:
        list: A list of dictionaries, each representing an object with
              'color' (int), 'coords' (set of (row, col) tuples),
              and 'min_coord' (tuple of (min_r, min_c)).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                # Initialize min_r/min_c here, will find true min later
                # min_r_init, min_c_init = r, c 

                queue = [(r, c)]
                visited[r,c] = True
                current_coords = set([(r,c)])

                while queue:
                    row, col = queue.pop(0)
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
                            current_coords.add((nr,nc))
                
                if current_coords:
                    obj_coords = current_coords
                    # Find the true minimum coordinate after collecting all coords
                    actual_min_r = min(r_coord for r_coord, c_coord in obj_coords)
                    actual_min_c = min(c_coord for r_coord, c_coord in obj_coords)
                    objects.append({
                        'color': color,
                        'coords': obj_coords,
                        'min_coord': (actual_min_r, actual_min_c)
                    })
    return objects

def get_shape_signature(obj_coords):
    """
    Calculates a canonical representation (signature) of an object's shape.
    The signature is based on the relative coordinates of the object's pixels
    from its top-left corner.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        frozenset: A frozenset of relative (dr, dc) coordinates, representing the shape.
                   Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)
    relative_coords = frozenset((r - min_r, c - min_c) for r, c in obj_coords)
    return relative_coords

def get_line_pixels_bresenham(r1, c1, r2, c2):
    """
    Generates all integer pixel coordinates on the line from (r1, c1) to (r2, c2)
    using Bresenham's line algorithm. Includes start and end points.
    """
    pixels = []
    r, c = r1, c1
    dr = abs(r2 - r1)
    dc = abs(c2 - c1)
    sr = 1 if r1 < r2 else -1
    sc = 1 if c1 < c2 else -1
    err = dc - dr

    while True:
        pixels.append((r, c))
        if r == r2 and c == c2:
            break # Reached the end point

        e2 = 2 * err
        moved_c = False # Flag to check if horizontal move happened
        
        # Check horizontal move first (arbitrary choice, could be vertical)
        if e2 > -dr: # Equivalent to e2 >= dy in some formulations where dy is negative
            err -= dr
            c += sc
            moved_c = True

        # Check if endpoint was reached *exactly* after the horizontal move
        # If so, and we also need a vertical move (e2 < dc), we skip the vertical move
        # to avoid overshooting or landing on a pixel not strictly on the ideal line path.
        # This handles diagonal movements landing perfectly on the corner.
        if r == r2 and c == c2 and moved_c : 
             continue 

        # Check vertical move
        if e2 < dc: # Equivalent to e2 <= dx in some formulations
            err += dc
            r += sr
            
    return pixels


def draw_line(grid, r1, c1, r2, c2, color):
    """
    Draws the intermediate points of a line between (r1, c1) and (r2, c2)
    on the grid with the specified color using Bresenham's algorithm.
    Only modifies pixels that are currently white (0).
    Does not draw the start or end points themselves.

    Args:
        grid (np.ndarray): The grid to draw on (modified in-place).
        r1, c1 (int): Coordinates of the starting point.
        r2, c2 (int): Coordinates of the ending point.
        color (int): The color to draw the line with.
    """
    rows, cols = grid.shape
    line_pixels = get_line_pixels_bresenham(r1, c1, r2, c2)

    # Iterate through points, excluding the first (start) and the last (end)
    if len(line_pixels) > 2:
        for i in range(1, len(line_pixels) - 1):
            r_pixel, c_pixel = line_pixels[i]
            
            # Check bounds and if the pixel is white
            if 0 <= r_pixel < rows and 0 <= c_pixel < cols:
                if grid[r_pixel, c_pixel] == 0:
                    grid[r_pixel, c_pixel] = color


def transform(input_grid):
    """
    Transforms the input grid by finding pairs of identical objects (non-white, non-blue),
    removing original blue pixels, and drawing blue lines between corresponding
    pixels of each pair using Bresenham's line drawing algorithm.

    Args:
        input_grid (np.ndarray): The input 2D numpy array.

    Returns:
        np.ndarray: The transformed 2D numpy array.
    """
    # 1. Initialize Output Grid
    output_grid = copy.deepcopy(input_grid)
    rows, cols = output_grid.shape

    # 2. Clear Existing Blue pixels (color 1) from the output grid
    output_grid[output_grid == 1] = 0

    # 3. Identify non-white (0), non-blue (1) objects in the *original* input grid
    objects = find_objects(input_grid, ignore_colors={0, 1})

    # 4 & 5. Group objects by color and shape signature
    objects_by_signature = defaultdict(list)
    for obj in objects:
        signature_key = (obj['color'], get_shape_signature(obj['coords']))
        if signature_key[1] is not None: # Ensure shape signature is valid
             objects_by_signature[signature_key].append(obj)

    # 6 & 7. Find pairs and connect them
    for signature_key, obj_list in objects_by_signature.items():
        if len(obj_list) == 2:
            # Found a pair
            obj_A, obj_B = obj_list[0], obj_list[1]

            # 7a. Determine translation between the pair based on top-left corners
            min_r_A, min_c_A = obj_A['min_coord']
            min_r_B, min_c_B = obj_B['min_coord']
            dr_obj = min_r_B - min_r_A
            dc_obj = min_c_B - min_c_A

            # 7b & 7c. Iterate through pixels of Object A and find corresponding in B
            # Ensure iteration order is consistent if needed, though set order is arbitrary
            # Sorting coords might make debugging easier if order mattered, but it shouldn't here.
            sorted_coords_A = sorted(list(obj_A['coords'])) 
            
            for r_A, c_A in sorted_coords_A:
                # Calculate the theoretical corresponding coordinate in B
                r_B_target = r_A + dr_obj
                c_B_target = c_A + dc_obj

                # Check if the corresponding pixel actually exists in Object B's coordinate set
                # This is crucial because the translation is based on min_coord,
                # ensuring the shape overlay works pixel by pixel.
                if (r_B_target, c_B_target) in obj_B['coords']:
                    # 7d & 7e. Draw a line between the corresponding points (r_A, c_A) and (r_B_target, c_B_target)
                    # The draw_line function handles only coloring white pixels (0) with blue (1)
                    # and skips drawing the start/end points.
                    draw_line(output_grid, r_A, c_A, r_B_target, c_B_target, 1) # Draw with blue (1)
                # else: # Optional: Add logging here if a corresponding point is unexpectedly missing
                    # print(f"Warning: Corresponding point ({r_B_target},{c_B_target}) not found in Object B for source point ({r_A},{c_A})")


    # 8. Final Output
    return output_grid