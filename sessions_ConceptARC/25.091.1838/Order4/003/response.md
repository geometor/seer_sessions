```python
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

def _find_objects(grid):
    """
    Finds connected components (objects) of non-background pixels and their internal holes.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'coords' (set of non-zero pixel coordinates),
              'internal_holes' (set of enclosed zero pixel coordinates),
              'colors' (set of non-zero color values), and 'has_gray' (boolean).
    """
    height, width = grid.shape
    visited = set()
    objects = []
    
    # First pass: Find connected non-zero components (object pixels)
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                # Found the start of a new non-zero component
                current_object_coords = set()
                current_object_colors = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    current_object_colors.add(grid[row, col])
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] != 0 and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if current_object_coords:
                    objects.append({
                        'coords': current_object_coords,
                        'colors': current_object_colors,
                        'has_gray': 5 in current_object_colors,
                        'bounding_box': (min_r, min_c, max_r, max_c),
                        'internal_holes': set() # To be filled later
                    })

    # Second pass: Identify internal holes for each object
    all_object_pixels = set().union(*[obj['coords'] for obj in objects])
    
    # Find all background pixels potentially reachable from the outer border
    reachable_background = set()
    q_background = deque()
    
    # Add all border background pixels to the queue
    for r in range(height):
        if grid[r, 0] == 0 and (r, 0) not in reachable_background:
             q_background.append((r, 0))
             reachable_background.add((r,0))
        if grid[r, width-1] == 0 and (r, width-1) not in reachable_background:
             q_background.append((r, width-1))
             reachable_background.add((r,width-1))
    for c in range(width):
        if grid[0, c] == 0 and (0, c) not in reachable_background:
             q_background.append((0, c))
             reachable_background.add((0,c))
        if grid[height-1, c] == 0 and (height-1, c) not in reachable_background:
             q_background.append((height-1, c))
             reachable_background.add((height-1,c))

    # BFS from border background pixels
    while q_background:
        r, c = q_background.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] == 0 and (nr, nc) not in reachable_background:
                reachable_background.add((nr, nc))
                q_background.append((nr, nc))

    # Assign internal holes to objects
    for obj in objects:
        min_r, min_c, max_r, max_c = obj['bounding_box']
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                # If a pixel is background(0), within the bounding box,
                # and NOT reachable from the outer border, it's an internal hole for *some* object.
                # We assume it belongs to the object defining this bounding box for simplicity in this task structure.
                # A more complex check might be needed if objects interleave holes.
                if grid[r,c] == 0 and (r,c) not in reachable_background and (r,c) not in all_object_pixels:
                     # Double check adjacency to *this* object's coords - improves robustness slightly
                     is_adjacent_to_this_obj = False
                     for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                         nr, nc = r + dr, c + dc
                         if (nr, nc) in obj['coords']:
                             is_adjacent_to_this_obj = True
                             break
                     if is_adjacent_to_this_obj:
                         obj['internal_holes'].add((r, c))

    return objects


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
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

    # Find all objects and their internal holes in the input grid
    objects = _find_objects(input_grid)

    # Process each object
    for obj in objects:
        coords = obj['coords']
        colors = obj['colors']
        has_gray = obj['has_gray']
        internal_holes = obj['internal_holes']
        
        primary_color = -1
        target_color = -1

        # Determine primary color and apply transformation map
        if has_gray:
            primary_colors = [c for c in colors if c != 0 and c != 5]
            if primary_colors: # Should have exactly one based on examples
                 primary_color = primary_colors[0]
                 target_color = map_gray_present.get(primary_color, primary_color) # Default to itself if not in map
            # else: handle unexpected case like only gray? Keep original color maybe?
            # target_color remains -1 or handle explicitly. For now assume valid primary.
            
        else: # No gray color (5) in the object
            primary_colors = [c for c in colors if c != 0]
            if len(primary_colors) == 1: # Should have exactly one based on examples
                primary_color = primary_colors[0]
                target_color = map_gray_absent.get(primary_color, primary_color) # Default to itself if not in map
            # else: handle unexpected case like multiple non-gray colors? Keep original?
            # target_color remains -1 or handle explicitly. For now assume valid primary.

        # Update the output grid for all pixels belonging to the object's footprint
        if target_color != -1: # Ensure we found a valid transformation target
            all_pixels_to_update = coords.union(internal_holes)
            for r, c in all_pixels_to_update:
                 # Bounds check just in case, though coords should be valid
                if 0 <= r < height and 0 <= c < width:
                    output_grid[r, c] = target_color
        # If target_color remained -1 (due to unexpected object composition),
        # the original colors in output_grid (copied from input) are preserved for that object.

    return output_grid
```