import numpy as np
from collections import deque

"""
Transformation rule based on observations:
1. Identify the background color (assumed to be the most frequent color, typically orange/7).
2. Find distinct contiguous objects touching the four main corners of the grid (top-left, top-right, bottom-left, bottom-right). Ignore background-colored objects.
3. Collect the unique colors of these corner objects. Let N be the number of unique colors.
4. Determine a 'target color' based on N and grid dimensions (H, W):
    - If N = 0: No non-background corner objects, no change.
    - If N = 1: Target color is the single unique color found.
    - If N = 2: Let colors be c1, c2 (sorted). If H and W are both odd, target is min(c1, c2). Otherwise, target is max(c1, c2).
    - If N = 3: Let colors be c1, c2, c3 (sorted). Target color is the median color (c2).
    - If N >= 4: Rule is undefined by examples, assume no change.
5. Identify all corner objects that match the 'target color'.
6. For each target object:
    - Determine its dimensions (height h, width w).
    - Determine its origin corner (TL, TR, BL, BR).
    - Calculate a move vector (dr, dc) based on origin corner and dimensions:
        - TL origin: dr = h, dc = w
        - TR origin: dr = h, dc = -w
        - BL origin: dr = -h, dc = w
        - BR origin: dr = -h, dc = -w
    - Move every pixel (r, c) of the object to (r + dr, c + dc).
7. Update the grid:
    - Set the original positions of all moved pixels to the background color.
    - Set the new positions to the target color, handling overlaps (last write wins, effectively).
"""

def _get_background_color(grid):
    """Determine the background color (most frequent)."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def _find_object_details_bfs(grid, start_row, start_col, visited, background_color):
    """
    Finds all coordinates, color, and dimensions of a connected object starting from (start_row, start_col) using BFS.
    Avoids searching the background color and already visited pixels.

    Args:
        grid (np.array): The input grid.
        start_row (int): Starting row index.
        start_col (int): Starting column index.
        visited (set): A set of (row, col) tuples already visited.
        background_color (int): The background color to ignore.

    Returns:
        tuple: (frozenset of (row, col) coordinates, object_color, height, width)
               Returns (None, None, None, None) if the start pixel is background, out of bounds, or already visited.
    """
    height, width = grid.shape

    if not (0 <= start_row < height and 0 <= start_col < width):
        return None, None, None, None # Start is out of bounds

    start_color = grid[start_row, start_col]

    if start_color == background_color or (start_row, start_col) in visited:
        return None, None, None, None # Don't process background or already processed parts

    q = deque([(start_row, start_col)])
    object_coords = set()
    visited.add((start_row, start_col)) # Mark start as visited

    min_r, max_r = start_row, start_row
    min_c, max_c = start_col, start_col

    while q:
        r, c = q.popleft()
        object_coords.add((r, c))
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)

        # Explore neighbors (4-directional)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, color match, and if not visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == start_color and (nr, nc) not in visited:
                visited.add((nr, nc)) # Mark visited when adding to queue
                q.append((nr, nc))

    obj_h = max_r - min_r + 1
    obj_w = max_c - min_c + 1

    return frozenset(object_coords), start_color, obj_h, obj_w

def _get_corner_objects_and_colors(grid, background_color):
    """
    Identifies objects touching the four corners of the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        tuple: (corner_objects, unique_colors)
            - corner_objects (dict): Maps color -> list of (coords, height, width) tuples.
            - unique_colors (list): Sorted list of unique colors found in corner objects.
    """
    height, width = grid.shape
    corners = [(0, 0), (0, width - 1), (height - 1, 0), (height - 1, width - 1)]
    corner_objects = {} # {color: [(coords, h, w), ...]}
    visited = set() # Shared visited set

    for r_corn, c_corn in corners:
        # Need to handle cases where the corner pixel itself might be background
        # but an object touches it. Search neighbors if corner is background.
        q = deque([(r_corn, c_corn)])
        potential_starts = set()
        
        # Check the corner itself first
        if grid[r_corn, c_corn] != background_color:
             potential_starts.add((r_corn, c_corn))
        else: # If corner is background, check its direct neighbors
             for dr in [-1, 0, 1]:
                 for dc in [-1, 0, 1]:
                     if dr == 0 and dc == 0: continue
                     nr, nc = r_corn + dr, c_corn + dc
                     if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] != background_color:
                         potential_starts.add((nr, nc))
                         
        processed_in_this_corner = set() # Track objects found from this corner check
        for r_start, c_start in potential_starts:
             if (r_start, c_start) in visited: continue # Already part of a found object

             coords, color, obj_h, obj_w = _find_object_details_bfs(grid, r_start, c_start, visited, background_color)
             
             if coords: # If a valid object was found
                 # Check if this object actually contains/touches one of the four corner pixels
                 is_corner_object = False
                 for cr, cc in corners:
                     # Check if corner pixel is in the object OR if object is adjacent to corner pixel
                     if (cr, cc) in coords:
                         is_corner_object = True
                         break
                     for dr in [-1, 0, 1]:
                         for dc in [-1, 0, 1]:
                             if dr==0 and dc==0: continue
                             if (cr+dr, cc+dc) in coords:
                                is_corner_object = True
                                break
                     if is_corner_object: break

                 if is_corner_object:
                    obj_data = (coords, obj_h, obj_w)
                    # Avoid adding duplicate objects found from different starting points near the same corner
                    if obj_data not in processed_in_this_corner:
                        if color not in corner_objects:
                            corner_objects[color] = []
                        corner_objects[color].append(obj_data)
                        processed_in_this_corner.add(obj_data)

    unique_colors = sorted(list(corner_objects.keys()))
    return corner_objects, unique_colors

def _determine_move_vector(obj_coords, obj_h, obj_w, H, W):
    """
    Determines the move vector based on which corner the object occupies and its dimensions.

    Args:
        obj_coords (frozenset): Set of (row, col) coordinates of the object.
        obj_h (int): Object height.
        obj_w (int): Object width.
        H (int): Grid height.
        W (int): Grid width.

    Returns:
        tuple: (dr, dc) representing the movement vector. Returns (0,0) if corner cannot be determined.
    """
    # Check which corner pixel is contained within the object's coordinates
    if (0, 0) in obj_coords: return (obj_h, obj_w)         # Top-left moves by (h, w)
    if (0, W - 1) in obj_coords: return (obj_h, -obj_w)    # Top-right moves by (h, -w)
    if (H - 1, 0) in obj_coords: return (-obj_h, obj_w)   # Bottom-left moves by (-h, w)
    if (H - 1, W - 1) in obj_coords: return (-obj_h, -obj_w)# Bottom-right moves by (-h, -w)

    # Fallback: Check adjacency if corner pixel isn't *in* the object, but object touches it.
    # This might be needed if an object is L-shaped around a corner.
    # Find the coordinate closest to each corner.
    min_r = min(r for r,c in obj_coords)
    min_c = min(c for r,c in obj_coords)
    max_r = max(r for r,c in obj_coords)
    max_c = max(c for r,c in obj_coords)

    touches_tl = min_r == 0 and min_c == 0
    touches_tr = min_r == 0 and max_c == W - 1
    touches_bl = max_r == H - 1 and min_c == 0
    touches_br = max_r == H - 1 and max_c == W - 1
    
    if touches_tl: return (obj_h, obj_w)
    if touches_tr: return (obj_h, -obj_w)
    if touches_bl: return (-obj_h, obj_w)
    if touches_br: return (-obj_h, -obj_w)

    # If still undetermined, return no move (shouldn't happen with _get_corner_objects logic)
    print(f"Warning: Could not determine corner for object with {len(obj_coords)} pixels. h={obj_h}, w={obj_w}. BBox: ({min_r},{min_c})-({max_r},{max_c})")
    return (0, 0)

def transform(input_grid):
    """
    Transforms the input grid by identifying corner objects, determining a target color
    based on the count of unique corner object colors and grid dimensions, and moving
    objects of the target color diagonally inwards by an amount determined by their dimensions.
    """
    # Determine background color
    background_color = _get_background_color(input_grid)
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)

    # 1. Identify corner objects and their unique colors
    # Need to refine _get_corner_objects to handle objects *touching* corners, not just containing the corner pixel
    corner_objects, unique_colors = _get_corner_objects_and_colors(input_grid, background_color)

    # 2. Determine the target color based on the number of unique colors (N)
    N = len(unique_colors)
    target_color = -1 # Default invalid color

    if N == 0:
        # No non-background corner objects found
        return output_grid
    elif N == 1:
        # If only one color, that's the target
        target_color = unique_colors[0]
    elif N == 2:
        # If two colors, check grid dimensions parity
        min_color, max_color = unique_colors[0], unique_colors[1]
        if height % 2 != 0 and width % 2 != 0: # Both dimensions odd
            target_color = min_color
        else: # At least one dimension is even
            target_color = max_color
    elif N == 3:
        # If three colors, target is the median
        target_color = unique_colors[1]
    else:
        # Rule for N=4 or more is undefined by examples, assume no move
        # print(f"Info: Found {N} unique corner colors. Rule undefined. No objects moved.")
        return output_grid # Return original grid if rule undefined

    # 3. Identify objects matching the target color
    target_object_data = corner_objects.get(target_color, []) # List of (coords, h, w)
    if not target_object_data:
        # Target color determined, but no objects of that color found
        return output_grid

    # 4. Prepare for moving objects
    pixels_to_clear = set()
    pixels_to_set = [] # List of (new_row, new_col, color)

    # 5. Calculate moves for each target object
    for obj_coords, obj_h, obj_w in target_object_data:
        # Determine movement vector for this object
        dr, dc = _determine_move_vector(obj_coords, obj_h, obj_w, height, width)

        if dr == 0 and dc == 0: continue # Skip if no move vector determined

        # Add all original pixels to the clear set
        pixels_to_clear.update(obj_coords)

        # Calculate new positions for all pixels in the object
        for r, c in obj_coords:
            nr, nc = r + dr, c + dc
            # Check if the new position is within grid bounds
            # (Out of bounds pixels simply disappear)
            if 0 <= nr < height and 0 <= nc < width:
                 pixels_to_set.append((nr, nc, target_color))

    # 6. Apply changes to the output grid
    # First, clear the original positions
    for r, c in pixels_to_clear:
        output_grid[r, c] = background_color

    # Then, set the new positions. Overlapping writes are handled implicitly (last one wins)
    for nr, nc, color in pixels_to_set:
        output_grid[nr, nc] = color # Assign target color

    return output_grid