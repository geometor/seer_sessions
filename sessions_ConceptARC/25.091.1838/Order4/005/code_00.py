import numpy as np
from collections import deque

"""
Transforms the input grid based on object colors and the presence of gray (5), filling internal holes.

1.  Identifies distinct objects in the input grid. An object consists of:
    *   A core set of connected non-white (non-zero) pixels ('Pixels').
    *   An optional set of enclosed white (0) pixels ('Internal_Holes') surrounded by the object's 'Pixels'.
2.  For each object, checks if gray (5) is present among its core pixels.
3.  Determines a 'primary color':
    *   If gray is present, it's the other non-white color.
    *   If gray is absent, it's the single non-white color.
4.  Applies one of two color transformation rules to the primary color based on gray's presence, yielding a 'target output color':
    *   Rule (Gray Present): Blue(1)->Yellow(4), Red(2)->Red(2), Yellow(4)->Green(3), Green(3)->Blue(1).
    *   Rule (Gray Absent): Yellow(4)->Magenta(6), Red(2)->Orange(7), Magenta(6)->Red(2), Orange(7)->Yellow(4).
5.  Updates the output grid by setting all pixels corresponding to the object's core ('Pixels') and its 'Internal_Holes' to the 'target output color'.
6.  External background pixels remain unchanged.
"""

def _find_objects_and_holes(grid):
    """
    Finds connected components (objects) of non-background pixels 
    and associates enclosed background pixels (internal holes) with them.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (set of non-zero pixel coordinates),
              'internal_holes' (set of enclosed zero pixel coordinates),
              'colors' (set of non-zero color values), and 'has_gray' (boolean).
    """
    height, width = grid.shape
    visited_objects = set()
    objects = []
    all_object_pixels = set()

    # --- Step 1: Find connected non-zero components (object pixels) ---
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited_objects:
                # Found the start of a new non-zero component
                current_object_coords = set()
                current_object_colors = set()
                q = deque([(r, c)])
                visited_objects.add((r, c))

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])
                    all_object_pixels.add((row, col)) # Keep track of all object pixels globally

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited_objects:
                            visited_objects.add((nr, nc))
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append({
                        'coords': current_object_coords,
                        'colors': current_object_colors,
                        'has_gray': 5 in current_object_colors,
                        'internal_holes': set() # Initialize hole set for this object
                    })

    # --- Step 2: Identify all background pixels reachable from the border ---
    reachable_background = set()
    q_background = deque()
    
    # Add all border background pixels to the queue if they are background(0)
    for r in range(height):
        if grid[r, 0] == 0: q_background.append((r, 0)); reachable_background.add((r,0))
        if grid[r, width-1] == 0: q_background.append((r, width-1)); reachable_background.add((r,width-1))
    # Avoid adding corners twice
    for c in range(1, width - 1): 
        if grid[0, c] == 0: q_background.append((0, c)); reachable_background.add((0,c))
        if grid[height-1, c] == 0: q_background.append((height-1, c)); reachable_background.add((height-1,c))

    # BFS from border background pixels to find all connected external background
    visited_background = set(reachable_background) # Use separate visited set for background BFS
    while q_background:
        r, c = q_background.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and (nr, nc) not in visited_background:
                visited_background.add((nr, nc))
                reachable_background.add((nr, nc))
                q_background.append((nr, nc))

    # --- Step 3: Identify internal holes and associate them with objects ---
    for r in range(height):
        for c in range(width):
            # If a pixel is background(0) and not reachable from the outside, it's an internal hole
            if grid[r, c] == 0 and (r, c) not in reachable_background:
                hole_coord = (r, c)
                # Find which object this hole belongs to by checking adjacent pixels
                adjacent_object_found = False
                for obj in objects:
                     # Check if any neighbor of the hole is part of this object's coordinates
                     is_adjacent = False
                     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = r + dr, c + dc
                         if (nr, nc) in obj['coords']:
                             is_adjacent = True
                             break
                     if is_adjacent:
                         obj['internal_holes'].add(hole_coord)
                         adjacent_object_found = True
                         # Assuming a hole belongs to only one object based on problem structure
                         break 
                # Optional: Handle case where a hole isn't adjacent to any identified object? 
                # This shouldn't happen if object finding is correct for ARC tasks.

    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the color transformation maps
    map_gray_present = {
        1: 4,  # Blue -> Yellow
        2: 2,  # Red -> Red
        4: 3,  # Yellow -> Green
        3: 1   # Green -> Blue
    }
    map_gray_absent = {
        4: 6,  # Yellow -> Magenta
        2: 7,  # Red -> Orange
        6: 2,  # Magenta -> Red
        7: 4   # Orange -> Yellow
    }

    # Find all objects and their associated internal holes
    objects = _find_objects_and_holes(input_grid)

    # Process each object
    for obj in objects:
        coords = obj['coords']
        colors = obj['colors']
        has_gray = obj['has_gray']
        internal_holes = obj['internal_holes']
        
        primary_color = -1
        target_color = -1

        # Determine primary color based on presence of gray
        if has_gray:
            # Find the non-gray, non-zero color
            primary_colors = [c for c in colors if c != 0 and c != 5]
            if primary_colors: # Should have exactly one based on examples
                 primary_color = primary_colors[0]
                 # Apply the transformation rule for objects with gray
                 target_color = map_gray_present.get(primary_color, primary_color) 
            else:
                 # Handle case of object being *only* gray (not seen in examples)
                 # Default: keep gray as gray? or treat as error? Keeping gray for now.
                 if colors == {5}:
                     target_color = 5 
            
        else: # No gray color (5) in the object
            # Find the single non-zero color
            primary_colors = [c for c in colors if c != 0]
            if len(primary_colors) == 1: # Should have exactly one based on examples
                primary_color = primary_colors[0]
                # Apply the transformation rule for objects without gray
                target_color = map_gray_absent.get(primary_color, primary_color) 
            # else: Handle case of multiple non-gray colors without gray (not seen in examples)
            # Default: Keep original colors by not setting target_color? For now assume valid input.

        # Update the output grid for all pixels in the object's footprint (coords + holes)
        if target_color != -1: # Ensure we found a valid transformation target
            all_pixels_to_update = coords.union(internal_holes)
            for r, c in all_pixels_to_update:
                 # Bounds check just for safety
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = target_color
        # If target_color remained -1 (due to unexpected object composition),
        # the original colors in output_grid (copied from input) are preserved for that object.

    return output_grid